"""Steps 5 and 6: strategies for updating an index on real embeddings.

The index starts from the first 100,000 texts of a dated corpus and receives another
100,000 in ten rounds of 10,000, in date order: the drift is the real one.

Datasets (embed_corpus.py): news, arxiv with all-MiniLM-L6-v2 (384 dimensions);
news-bge, arxiv-bge with bge-base-en-v1.5 (768 dimensions).

Measures, at the reported rounds:
  error in the lists: every text stays in the list it was inserted into
  recall@10:          for the texts held out of the index, the nearest lists are
                      probed until exactly a given share of the index has been read
                      (0.1% and 1%); we count how many candidates are at least as
                      close as the true tenth, so duplicates and ties do not count
                      as errors
For the strategies on the new texts only we also measure what happens when all the
vectors are reassigned to the updated centroids ("+ lists rebuilt"). The rebuild is
done only once, at the reported round, on the centroids obtained without ever
rebuilding before: it is not the same as rebuilding after every update.
When the read limit falls inside a list, its texts are read in random order, so
the most recent ones are not at a disadvantage.

The queries are texts from the corpus, not user questions: the recall holds for
"find similar texts". Only those dated within the period covered by the index are
used, so their number grows at every round.

It breaks down the causes of the damage of the naive use of e-means (old centroids
as the start, training on the new texts only) by switching three things on and off:
the initial mass of the centroids, the revival of clusters, the final means.
The three things interact: without mass, revival recycles hundreds of valid
centroids, with mass only the really small lists; with the final means the mass
matters little. The table must be read by combinations, not as a sum of three effects.

"Mass" has two units. In the breakdown and on the new texts only it is step × number
of texts in the list: the first update is equivalent to the mean with the true counts.
In the strategies that reread everything it is the steady-state mass, batch × share
of the list: the one the centroid would have in a run already under way.

No-drift control: the same texts in random order, index never updated.

The timings of the full rebuild are in bench_rebuild.py, which must be run on its own.

Usage: uv run exp_real.py news > results/exp_real_news.md
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

from emeans import INIT_MASS, batch_law, emeans, step_law
from exp_new_only import online_mean
from exp_rule import warm
from exp_sequence import list_mse
from exp_warm import assign_all

K = 2048  # 4 · square root of 200,000, rounded to a power of two, as in Appendix L of the paper
N0, ROUNDS, CHUNK, N_QUERIES = 100_000, 10, 10_000, 3_000
REPORT = (1, 5, 10)
assert REPORT[-1] == ROUNDS
SEEDS = (0, 1, 2)
BUDGETS, TOP = (0.001, 0.01), 10
D = None  # dimension of the embeddings, set by load()

STALE = "never update"
FAISS_NAIVE = "Faiss 1.16.0 e-means, default settings"
ONLINE = "mini-batch k-means from the list sizes"
TUNED = "e-means: mass 0.2, step/4, no revival, no final means"
REFERENCE = "from scratch, 10 epochs (reference)"
CONTROL = "never update, texts in random order (no-drift control)"
# name: (epochs, steady-state mass, final means). They reread everything at every round, restarting from their own centroids.
WARM = {
    "warm start, 1 epoch per round": (1, False, True),
    "warm start, 3 epochs per round": (3, False, True),
    "warm start with steady-state mass, 3 epochs per round": (3, True, True),
    "warm start with steady-state mass, no final means, 3 epochs per round": (3, True, False),
}
COLD = {"from scratch, 1 epoch": 1, "from scratch, 3 epochs": 3, REFERENCE: 10}


def ablation_name(mass, revival, closing):
    yes = lambda flag: "yes" if flag else "no"
    return f"e-means: mass {yes(mass)}, revival {yes(revival)}, final means {yes(closing)}"


def ablation(mass, revival, closing):
    """e-means on the new texts only from the old centroids, with three switches."""
    def update(centroids, counts, added, seed):
        alpha0 = step_law(len(added), K, 1, batch_law(len(added), K, 1, D))
        init_mass = np.maximum(alpha0 * counts, INIT_MASS) if mass else INIT_MASS
        return emeans(added, K, epochs=1, seed=seed, init=centroids, init_mass=init_mass,
                      tau=0.1 if revival else 0.0, finalize=closing)
    return update


def faiss_naive(centroids, counts, added, seed):
    trained, _ = NumpyEmeans(D, K, nepochs=1, seed=seed).train(
        np.ascontiguousarray(added, dtype=np.float32), init_centroids=centroids.astype(np.float32))
    return trained.astype(np.float64)


# name: update(centroids, list sizes, new texts, seed). They read only the new texts.
NEW_ONLY = {
    STALE: lambda c, counts, added, seed: c,
    FAISS_NAIVE: faiss_naive,
    **{ablation_name(*flags): ablation(*flags) for flags in itertools.product((False, True), (True, False), (True, False))},
    ONLINE: lambda c, counts, added, seed: online_mean(added, c, counts, batch_law(len(added), K, 1, D), seed),
    TUNED: lambda c, counts, added, seed: warm(added, c, counts, 0.2, seed),
}


def tenth_score(index, queries):
    """Similarity of the TOP-th nearest text to every query. Normalised vectors: the dot product is enough."""
    out = []
    for start in range(0, len(queries), 500):
        scores = queries[start : start + 500] @ index.T
        out.append(np.partition(scores, -TOP, axis=1)[:, -TOP])
    return np.concatenate(out)


def recall(index, labels, centroids, queries, threshold, budgets=BUDGETS, nprobe=None):
    """How many of the true TOP are found, for every query and for every share of the index read.

    Returns integers between 0 and TOP, of shape (shares, queries). With nprobe,
    exactly nprobe whole lists are probed instead (needed for the comparison with Faiss).
    """
    # inside every list the texts are in random order: a partly read list does not favour the oldest ones
    order = np.lexsort((np.random.default_rng(0).random(len(labels)), labels))
    ends = np.cumsum(np.bincount(labels, minlength=K))
    starts = ends - np.bincount(labels, minlength=K)
    ranking = np.argsort(assign_scores(queries, centroids), axis=1)
    limits = [len(index)] if nprobe else [int(b * len(index)) for b in budgets]
    found = np.zeros((len(limits), len(queries)), dtype=np.uint8)
    for i, query in enumerate(queries):
        candidates, left = [], max(limits)
        for j in ranking[i][:nprobe]:
            members = order[starts[j] : ends[j]][:left]  # the last list is read only in part
            candidates.append(members)
            left -= len(members)
            if left == 0:
                break
        hits = index[np.concatenate(candidates)] @ query >= threshold[i] - 1e-6
        for b, limit in enumerate(limits):
            found[b, i] = min(int(hits[:limit].sum()), TOP)
    return found


def assign_scores(queries, centroids):
    """Squared distance from every centroid, up to a constant per query."""
    centroids = centroids.astype(np.float32)
    return (centroids**2).sum(1)[None, :] - 2.0 * queries @ centroids.T


def load(corpus="news"):
    global D
    x = np.load(f"data/{corpus}_embeddings.npy")
    dates = np.load(f"data/{corpus}_dates.npy")
    D = x.shape[1]
    assert len(x) == len(dates) >= N0 + ROUNDS * CHUNK + N_QUERIES
    assert (dates[1:] >= dates[:-1]).all(), "the texts must be in date order"
    held = np.zeros(len(x), dtype=bool)
    held[np.random.default_rng(0).choice(len(x), N_QUERIES, replace=False)] = True
    docs, doc_dates = x[~held][: N0 + ROUNDS * CHUNK], dates[~held][: N0 + ROUNDS * CHUNK]
    return docs, doc_dates, x[held], dates[held]


def run(seed, docs, doc_dates, queries, query_dates):
    """Returns the numbers per strategy and round, and the query-by-query results."""
    docs64 = docs.astype(np.float64)
    old = docs64[:N0]
    start = emeans(old, K, epochs=5, seed=seed)
    start_labels = assign_all(old, start)[0]
    state = {name: (start, start_labels) for name in (*NEW_ONLY, *WARM)}
    out, per_query = {}, {}
    for r in range(1, ROUNDS + 1):
        n = N0 + r * CHUNK
        seen, added = docs64[:n], docs64[n - CHUNK : n]
        for name, update in NEW_ONLY.items():
            centroids, labels = state[name]
            counts = np.bincount(labels, minlength=K).astype(np.float64)
            centroids = update(centroids, counts, added, 1000 * seed + r)
            state[name] = centroids, np.concatenate([labels, assign_all(added, centroids)[0]])
        for name, (epochs, with_mass, closing) in WARM.items():
            centroids, labels = state[name]
            init_mass = INIT_MASS
            if with_mass:  # mass the centroids would have in a run already in steady state
                batch = batch_law(n, K, epochs, D)
                init_mass = np.maximum(batch * np.bincount(labels, minlength=K) / n, INIT_MASS)
            centroids = emeans(seen, K, epochs=epochs, seed=1000 * seed + r, init=centroids, init_mass=init_mass, finalize=closing)
            state[name] = centroids, assign_all(seen, centroids)[0]
        if r not in REPORT:
            continue
        indexes = dict(state)
        for name, epochs in COLD.items():
            centroids = emeans(seen, K, epochs=epochs, seed=1000 * seed + r)
            indexes[name] = centroids, assign_all(seen, centroids)[0]
        reference = list_mse(seen, *indexes[REFERENCE])
        # queries from the period the index covers, split between the initial period and the added period
        usable = query_dates <= doc_dates[n - 1]
        recent = query_dates[usable] > doc_dates[N0 - 1]
        threshold = tenth_score(docs[:n], queries[usable])

        def measure(name, index, index64, centroids, labels):
            found = recall(index, labels, centroids, queries[usable], threshold)
            per_query[f"{r}|{name}"] = found
            out.setdefault(name, {})[r] = {
                "error": 100 * (list_mse(index64, centroids, labels) / reference - 1),
                **{f"recall {b:.1%}": float(found[i].mean()) / TOP for i, b in enumerate(BUDGETS)},
                "recall added": float(found[-1][recent].mean()) / TOP,
                "queries": int(usable.sum()),
                "queries added": int(recent.sum()),
                "absolute error of the reference": reference,
            }

        for name, (centroids, labels) in indexes.items():
            measure(name, docs[:n], seen, centroids, labels)
            if name in NEW_ONLY and name != STALE:  # what if the lists were rebuilt after the update?
                measure(name + " + lists rebuilt", docs[:n], seen, centroids, assign_all(seen, centroids)[0])
        per_query[f"{r}|recent"] = recent
    # No-drift control: same texts, random order, centroids of the first N0 and never updated.
    order = np.random.default_rng(seed).permutation(len(docs))
    centroids = emeans(docs64[order[:N0]], K, epochs=5, seed=seed)
    measure(CONTROL, docs[order], docs64[order], centroids, assign_all(docs64[order], centroids)[0])
    out[CONTROL][ROUNDS]["recall added"] = float("nan")  # in random order the date distinguishes nothing
    return out, per_query


if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    print(f"Dataset: {corpus}, {D} dimensions.")
    print(f"Initial index: {N0} texts, from {doc_dates[0]} to {doc_dates[N0 - 1]}.")
    print(f"{ROUNDS} rounds of {CHUNK} texts, up to {doc_dates[-1]}. {K} lists, {len(SEEDS)} algorithm seeds.")
    print(f"Recall@{TOP} reading 0.1% and 1% of the index. Median over {len(SEEDS)} seeds. The intervals are in results/SUMMARY.md.\n")
    runs, arrays = [], {}
    for seed in SEEDS:
        out, per_query = run(seed, docs, doc_dates, queries, query_dates)
        runs.append(out)
        arrays.update({f"{seed}|{key}": value for key, value in per_query.items()})
        # saved after every seed: a stop halfway does not lose the work done
        Path(f"results/exp_real_{corpus}.json").write_text(json.dumps(runs))
        np.savez_compressed(f"results/exp_real_{corpus}.npz", **arrays)
    med = lambda name, r, key: np.median([run_[name][r][key] for run_ in runs])
    for r in REPORT:
        row = runs[0][REFERENCE][r]
        print(
            f"\n### After {r} round{'' if r == 1 else 's'} (index up to {doc_dates[N0 + r * CHUNK - 1]}; "
            f"{row['queries']} queries, of which {row['queries added']} from the added period)\n"
        )
        print("| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |")
        print("|---|---|---|---|---|")
        for name in runs[0]:
            if r in runs[0][name]:
                print(
                    f"| {name} | {med(name, r, 'error'):+.2f}% | {med(name, r, 'recall 0.1%'):.3f} | "
                    f"{med(name, r, 'recall 1.0%'):.3f} | {'—' if name == CONTROL else format(med(name, r, 'recall added'), '.3f')} |"
                )
