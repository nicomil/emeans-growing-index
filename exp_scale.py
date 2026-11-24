"""The experiment of exp_real.py taken to a larger scale, with Faiss code only.

An IVF index built on the first texts in date order receives ROUNDS blocks of more
recent texts. Strategies:

  - never update the centroids;
  - Faiss e-means on the new texts only, starting from the old centroids (naive use);
  - Faiss k-means, one iteration on the new texts only from the old centroids;
  - Faiss e-means with initial mass and read-out of the moving average;
  - rebuild from scratch on all texts, e-means at 3 epochs; at the end of the run also at 10 (reference);
  - DeDrift (Baranchuk et al., ICCV 2023), rewritten from the text of the paper, section 5.1, because
    no published code could be found. Lazy: every centroid becomes the mean of the vectors of its
    list, without moving vectors. Split: the vectors of the k largest lists and of the k2 - k
    smallest ones are clustered again with k-means into k2 lists, with k2 chosen so that the new
    lists have the median size; the other lists do not change. Hybrid: Lazy, then Split.
    Here k = centroids / 256 (in the paper 8 with 4,096 centroids and 64 with 16,384) and one update
    at every round. The paper does not say how many k-means iterations Split uses nor how it is
    initialised: here 10, with the random initialisation of Faiss.

For the strategies that read only the new texts the recall is measured in two ways: with the
vectors kept in the list they entered, and with the lists rebuilt at the time of the
measurement. The recall is that of exp_real.py: true TOP neighbours found by reading a fixed
share of the index. The time of every operation is recorded: training of the centroids and
reassignment of all the vectors are kept separate.

Differences from exp_real.py, to cope with the scale: everything in single precision, assignments
and true neighbours computed with Faiss IndexFlat, initial index trained with NumpyEmeans
(5 epochs) instead of the NumPy rewrite.

Usage: uv run exp_scale.py arxiv-full [seed] > results/exp_scale_arxiv-full_seed0.md
       uv run exp_scale.py arxiv 0 small       # same scale as exp_real.py, for comparison
"""

import json
import sys
import time
from pathlib import Path

import faiss
import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

import exp_real
from exp_real import BUDGETS, TOP, recall

SCALES = {  # name: (initial texts, rounds, texts per round, centroids)
    "large": (800_000, 10, 75_000, 16_384),
    "small": (100_000, 10, 10_000, 2_048),
}
N_QUERIES = 3_000
REPORT = (1, 5, 10)

STALE = "never update"
NAIVE = "Faiss e-means on the new texts, from the old centroids (naive use)"
LLOYD = "Faiss k-means on the new texts, one iteration from the old centroids"
FIXED = "Faiss e-means with initial mass and moving average"
COLD = "from scratch on all texts, e-means 3 epochs"
REFERENCE = "from scratch on all texts, e-means 10 epochs (reference)"
REBUILT = " + lists rebuilt"
FROM_SCRATCH = ((COLD, 3), (REFERENCE, 10))


def assign(x, centroids):
    """List of every vector: the nearest centroid."""
    index = faiss.IndexFlatL2(centroids.shape[1])
    index.add(centroids)
    return np.concatenate([index.search(x[i : i + 100_000], 1)[1][:, 0] for i in range(0, len(x), 100_000)])


def tenth_score(docs, queries):
    """Similarity of the TOP-th true neighbour. The vectors are normalised: the dot product is enough."""
    index = faiss.IndexFlatIP(docs.shape[1])
    index.add(docs)
    return index.search(queries, TOP)[0][:, -1]


def naive(centroids, counts, added, seed):
    return NumpyEmeans(added.shape[1], len(centroids), nepochs=1, seed=seed).train(added, init_centroids=centroids)[0]


def lloyd(centroids, counts, added, seed):
    kmeans = faiss.Kmeans(added.shape[1], len(centroids), niter=1, seed=seed + 1, max_points_per_centroid=len(added))
    kmeans.train(added, init_centroids=centroids)
    return kmeans.centroids


def fixed(centroids, counts, added, seed):
    em = NumpyEmeans(added.shape[1], len(centroids), nepochs=1, seed=seed)
    em.begin(len(added), centroids)
    em._usage[:] = em.recipe["alpha0"] * counts
    order = np.random.RandomState(seed).permutation(len(added))
    batch = em.recipe["batch_size"]
    for start in range(0, len(added), batch):
        em.update(em.accumulate(added[order[start : start + batch]]))
    return em.current_centroids()


def lazy(centroids, labels, seen, seed):
    """Every centroid becomes the mean of its own list; empty lists stay where they are."""
    order = np.argsort(labels, kind="stable")
    sizes = np.bincount(labels, minlength=len(centroids))
    filled = np.flatnonzero(sizes)
    sums = np.add.reduceat(seen[order], (np.cumsum(sizes) - sizes)[filled], axis=0)
    centroids = centroids.copy()
    centroids[filled] = sums / sizes[filled, None]
    return centroids, labels


def split(centroids, labels, seen, seed, niter=10, warm=False):
    """Clusters the largest lists again, together with as many small lists as needed to keep K unchanged.

    With warm, k-means starts from the old centroids of the lists involved instead of from random points.
    """
    k = max(1, len(centroids) // 256)
    sizes = np.bincount(labels, minlength=len(centroids))
    by_size = np.argsort(sizes, kind="stable")
    k2 = int(np.ceil(sizes[by_size[-k:]].sum() / np.median(sizes)))
    if k2 <= k:
        return centroids, labels
    involved = np.concatenate([by_size[-k:], by_size[: k2 - k]])
    rows = np.flatnonzero(np.isin(labels, involved))
    kmeans = faiss.Kmeans(seen.shape[1], k2, niter=niter, seed=seed + 1)
    kmeans.train(seen[rows], init_centroids=centroids[involved] if warm else None)
    centroids, labels = centroids.copy(), labels.copy()
    centroids[involved] = kmeans.centroids
    labels[rows] = involved[assign(seen[rows], kmeans.centroids)]
    return centroids, labels


DEDRIFT = {
    "DeDrift-Lazy": lazy,
    "DeDrift-Split": split,
    "DeDrift-Hybrid": lambda c, labels, seen, seed: split(*lazy(c, labels, seen, seed), seen, seed),
}

NEW_ONLY = {STALE: lambda c, counts, added, seed: c, NAIVE: naive, LLOYD: lloyd, FIXED: fixed}


def timed(function, *args):
    start = time.perf_counter()
    out = function(*args)
    return out, time.perf_counter() - start


def load(corpus, n_docs):
    x = np.load(f"data/{corpus}_embeddings.npy", mmap_mode="r")
    dates = np.load(f"data/{corpus}_dates.npy")
    assert len(x) == len(dates) >= n_docs + N_QUERIES
    assert (dates[1:] >= dates[:-1]).all(), "the texts must be in date order"
    asked = Path(f"data/{corpus}_queries.npy")
    if asked.exists():  # real user questions instead of the held-out texts
        queries = np.load(asked)[:N_QUERIES]
        when = Path(f"data/{corpus}_query_dates.npy")  # without it the questions count as asked at the end
        query_dates = np.load(when)[:N_QUERIES] if when.exists() else np.full(len(queries), dates[n_docs - 1])
        return np.ascontiguousarray(x[:n_docs]), dates[:n_docs], queries, query_dates
    held = np.zeros(len(x), dtype=bool)
    held[np.random.default_rng(0).choice(len(x), N_QUERIES, replace=False)] = True
    kept = np.flatnonzero(~held)[:n_docs]
    return np.ascontiguousarray(x[kept]), dates[kept], np.ascontiguousarray(x[held]), dates[held]


def run(corpus, seed, scale):
    n0, rounds, chunk, k = SCALES[scale]
    exp_real.K = k  # recall() in exp_real reads the number of lists from there
    docs, doc_dates, queries, query_dates = load(corpus, n0 + rounds * chunk)
    d = docs.shape[1]
    train = lambda x, epochs, s: np.ascontiguousarray(NumpyEmeans(d, k, nepochs=epochs, seed=s).train(x)[0])
    rows, per_query, times = [], {}, {}
    start, times["initial index: training, 5 epochs"] = timed(train, docs[:n0], 5, seed)
    start_labels, times["initial index: assignment"] = timed(assign, docs[:n0], start)
    state = {name: (start, start_labels) for name in (*NEW_ONLY, *DEDRIFT)}
    for r in range(1, rounds + 1):
        n = n0 + r * chunk
        added = docs[n - chunk : n]
        for name, update in NEW_ONLY.items():
            centroids, labels = state[name]
            counts = np.bincount(labels, minlength=k).astype(np.float32)
            centroids, seconds = timed(update, centroids, counts, added, 1000 * seed + r)
            centroids = np.ascontiguousarray(centroids, dtype=np.float32)
            times.setdefault(f"update on the new texts: {name}", []).append(seconds)
            state[name] = centroids, np.concatenate([labels, assign(added, centroids)])
        seen = docs[:n]
        for name, update in DEDRIFT.items():  # the new texts enter the index, then the index adjusts itself
            centroids, labels = state[name]
            labels = np.concatenate([labels, assign(added, centroids)])
            state[name], seconds = timed(update, centroids, labels, seen, 1000 * seed + r)
            times.setdefault(f"index update: {name}", []).append(seconds)
        if r not in REPORT:
            continue
        indexes = dict(state)
        for name in (NAIVE, LLOYD, FIXED):
            if name not in state:
                continue
            labels, seconds = timed(assign, seen, state[name][0])
            indexes[name + REBUILT] = state[name][0], labels
            times.setdefault("reassignment of all vectors", []).append((n, seconds))
        for name, epochs in FROM_SCRATCH:
            if epochs == 10 and r != rounds:
                continue
            centroids, seconds = timed(train, seen, epochs, 1000 * seed + r)
            times.setdefault(f"training: {name}", []).append((n, seconds))
            indexes[name] = centroids, assign(seen, centroids)
        usable = query_dates <= doc_dates[n - 1]
        late = usable & (query_dates > doc_dates[n0 - 1])
        threshold = tenth_score(seen, queries[usable])
        for name, (centroids, labels) in indexes.items():
            found = recall(seen, labels, centroids, queries[usable], threshold)
            per_query[f"{name}|{r}"] = found
            sizes = np.bincount(labels, minlength=k)
            rows.append({
                "round": r, "texts": n, "strategy": name, "queries": int(usable.sum()),
                **{f"recall {b}": float(found[i].mean()) / TOP for i, b in enumerate(BUDGETS)},
                "recall 0.01, added period": float(found[-1][late[usable]].mean()) / TOP,
                "imbalance": float(k * (sizes.astype(np.float64) ** 2).sum() / n**2),
            })
            print(f"round {r}: {name}: {rows[-1]['recall 0.01']:.3f}", file=sys.stderr, flush=True)
    return rows, per_query, times, (n0, rounds, chunk, k, d)


if __name__ == "__main__":
    corpus = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    scale = sys.argv[3] if len(sys.argv) > 3 else "large"
    rows, per_query, times, (n0, rounds, chunk, k, d) = run(corpus, seed, scale)
    main = "_main" if hasattr(faiss, "accumulate_removal_stats") else ""  # function present only after 1.16.0
    stem = f"results/exp_scale_{corpus}_seed{seed}" + ("" if scale == "large" else f"_{scale}") + main
    json.dump({"rows": rows, "times": times, "faiss": faiss.__version__}, open(stem + ".json", "w"), ensure_ascii=False, indent=1)
    np.savez_compressed(stem + ".npz", **per_query)

    print(f"Dataset: {corpus}, seed {seed}. {n0} initial texts, {rounds} rounds of {chunk}, {k} centroids, {d} dimensions.")
    print(f"Faiss {faiss.__version__}{' (main branch, built from source)' if main else ''}. Recall@{TOP}; a single seed, no intervals.\n")
    print("| Strategy | " + " | ".join(f"Round {r}: 1% read" for r in REPORT) + f" | Round {rounds}: added period | Round {rounds}: 0.1% read | Imbalance |")
    print("|---|" + "---|" * (len(REPORT) + 3))
    by = {(row["strategy"], row["round"]): row for row in rows}
    for name in dict.fromkeys(row["strategy"] for row in rows):
        cells = [f"{by[name, r]['recall 0.01']:.3f}" if (name, r) in by else "—" for r in REPORT]
        last = by[name, rounds]
        print(f"| {name} | " + " | ".join(cells) + f" | {last['recall 0.01, added period']:.3f} | {last['recall 0.001']:.3f} | {last['imbalance']:.2f} |")
    print("\nTimes in seconds (measured inside the experiment: indicative if the machine was doing something else).\n")
    print("| Operation | Time |")
    print("|---|---|")
    for name, value in times.items():
        if isinstance(value, float):
            print(f"| {name} | {value:.1f} |")
        elif isinstance(value[0], tuple):
            for n, seconds in dict(value).items():  # per number of texts: the last measurement
                print(f"| {name}, {n} texts | {seconds:.1f} |")
        else:
            print(f"| {name}, median over {len(value)} rounds | {np.median(value):.1f} |")
