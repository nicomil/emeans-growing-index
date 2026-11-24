"""The naive use of e-means and its fix, done with the Faiss code.

The collapse of the recall was also measured with emeans.py, our rewrite.
Here the same update on the new texts only is done with NumpyEmeans of Faiss 1.16.0:

  naive: NumpyEmeans.train(new, init_centroids=old), without touching anything;
  fixed: the same pass driven by hand with begin / accumulate / update,
         changing two things: the initial mass (step × number of texts in the
         list, written into the private attribute _usage, because there is no
         public way) and the read-out of the centroids (current_centroids, i.e. the
         moving average, instead of the final means of finalize).

If the fixed version with the Faiss code gives the same recall as our rewrite
with mass and without final means, the cause is demonstrated inside Faiss.

Usage: uv run check_faiss_naive.py news > results/check_faiss_naive_news.md
"""

import sys

import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

import exp_real
from emeans import emeans
from exp_real import BUDGETS, CHUNK, K, N0, REPORT, ROUNDS, SEEDS, TOP, ablation, load, recall, tenth_score
from exp_warm import assign_all


def faiss_naive(centroids, counts, added, seed):
    trained, _ = NumpyEmeans(exp_real.D, K, nepochs=1, seed=seed).train(added, init_centroids=centroids.astype(np.float32))
    return trained.astype(np.float64)


def faiss_fixed(centroids, counts, added, seed):
    """Same pass, with initial mass and read-out of the moving average. Faiss code only."""
    em = NumpyEmeans(exp_real.D, K, nepochs=1, seed=seed)
    em.begin(len(added), centroids.astype(np.float32))
    em._usage[:] = em.recipe["alpha0"] * counts
    order = np.random.RandomState(seed).permutation(len(added))
    batch = em.recipe["batch_size"]
    for start in range(0, len(added), batch):
        em.update(em.accumulate(added[order[start : start + batch]]))
    return em.current_centroids().astype(np.float64)


UPDATES = {
    "never update": lambda c, counts, added, seed: c,
    "Faiss, naive: train(new, init_centroids=old)": faiss_naive,
    "Faiss, with initial mass and read-out of the moving average": faiss_fixed,
    "our rewrite, naive": ablation(False, True, True),
    "our rewrite, with mass and without final means": ablation(True, True, False),
}

if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    docs64 = docs.astype(np.float64)
    one = len(BUDGETS) - 1
    results = {name: {r: [] for r in REPORT} for name in UPDATES}
    for seed in SEEDS:
        start = emeans(docs64[:N0], K, epochs=5, seed=seed)
        start_labels = assign_all(docs64[:N0], start)[0]
        state = {name: (start, start_labels) for name in UPDATES}
        for r in range(1, ROUNDS + 1):
            n = N0 + r * CHUNK
            for name, update in UPDATES.items():
                centroids, labels = state[name]
                counts = np.bincount(labels, minlength=K).astype(np.float64)
                added = docs64[n - CHUNK : n] if name.startswith(("our", "never")) else np.ascontiguousarray(docs[n - CHUNK : n])
                centroids = update(centroids, counts, added, 1000 * seed + r)
                state[name] = centroids, np.concatenate([labels, assign_all(docs64[n - CHUNK : n], centroids)[0]])
            if r in REPORT:
                usable = query_dates <= doc_dates[n - 1]
                threshold = tenth_score(docs[:n], queries[usable])
                for name, (centroids, labels) in state.items():
                    found = recall(docs[:n], labels, centroids, queries[usable], threshold)
                    results[name][r].append(float(found[one].mean()) / TOP)
    print(f"Dataset: {corpus}. Recall@{TOP} reading 1% of the index, lists kept as they are, median [min; max] over {len(SEEDS)} seeds.\n")
    print("| Update on the new texts only | " + " | ".join(f"After {r} round{'' if r == 1 else 's'}" for r in REPORT) + " |")
    print("|---|" + "---|" * len(REPORT))
    for name, by_round in results.items():
        cells = [f"{np.median(v):.3f} [{min(v):.3f}; {max(v):.3f}]" for v in by_round.values()]
        print(f"| {name} | " + " | ".join(cells) + " |")
