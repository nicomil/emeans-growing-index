"""How much of the damage of the naive use is specific to e-means, and how does it change with the size of the update?

A single update of an index of 100,000 texts, with 10,000 or 50,000 new texts
(about 5 and about 24 per centroid). The centroids are updated by reading only
the new texts, in six ways, all with Faiss code except the last:

  e-means, train(new, init_centroids=old)             the naive use
  e-means on the new texts, from random rows          without any old centroid
  k-means, one iteration from the old centroids       the generic comparison
  e-means with initial mass and moving average        the fix
  mini-batch k-means from the list sizes              our implementation

The recall@10 is measured reading 1% of the index, with the lists rebuilt and with
the lists kept as they are.

Usage: uv run check_naive_baselines.py news > results/check_naive_baselines_news.md
"""

import sys

import faiss
import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

import exp_real
from check_faiss_naive import faiss_fixed, faiss_naive
from emeans import batch_law, emeans
from exp_new_only import online_mean
from exp_real import BUDGETS, K, N0, SEEDS, TOP, load, recall, tenth_score
from exp_warm import assign_all

SIZES = (10_000, 50_000)


def faiss_scratch(centroids, counts, added, seed):
    return NumpyEmeans(exp_real.D, K, nepochs=1, seed=seed).train(added)[0].astype(np.float64)


def faiss_lloyd(centroids, counts, added, seed):
    kmeans = faiss.Kmeans(exp_real.D, K, niter=1, seed=seed + 1, max_points_per_centroid=len(added))
    kmeans.train(added, init_centroids=centroids.astype(np.float32))
    return kmeans.centroids.astype(np.float64)


UPDATES = {
    "never update": lambda c, counts, added, seed: c,
    "Faiss e-means: train(new, init_centroids=old)": faiss_naive,
    "Faiss e-means on the new texts, from random rows": faiss_scratch,
    "Faiss k-means on the new texts, one iteration from the old centroids": faiss_lloyd,
    "Faiss e-means with initial mass and moving average": faiss_fixed,
    "mini-batch k-means from the list sizes": lambda c, counts, added, seed: online_mean(
        added.astype(np.float64), c, counts, batch_law(len(added), K, 1, exp_real.D), seed),
}

if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    docs64 = docs.astype(np.float64)
    one = len(BUDGETS) - 1
    results = {(size, name): {"rebuilt": [], "kept": []} for size in SIZES for name in UPDATES}
    for seed in SEEDS:
        start = emeans(docs64[:N0], K, epochs=5, seed=seed)
        start_labels = assign_all(docs64[:N0], start)[0]
        counts = np.bincount(start_labels, minlength=K).astype(np.float64)
        for size in SIZES:
            n = N0 + size
            added = np.ascontiguousarray(docs[N0:n])
            usable = query_dates <= doc_dates[n - 1]
            threshold = tenth_score(docs[:n], queries[usable])
            for name, update in UPDATES.items():
                centroids = update(start, counts, added, 1000 * seed)
                kept = np.concatenate([start_labels, assign_all(docs64[N0:n], centroids)[0]])
                for key, labels in (("rebuilt", assign_all(docs64[:n], centroids)[0]), ("kept", kept)):
                    found = recall(docs[:n], labels, centroids, queries[usable], threshold)
                    results[(size, name)][key].append(float(found[one].mean()) / TOP)
    cell = lambda v: f"{np.median(v):.3f} [{min(v):.3f}; {max(v):.3f}]"
    print(f"Dataset: {corpus}. One update of an index of {N0} texts, {K} centroids.")
    print(f"Recall@{TOP} reading 1% of the index, median [min; max] over {len(SEEDS)} seeds.")
    for size in SIZES:
        print(f"\n### {size} new texts (about {size / K:.0f} per centroid)\n")
        print("| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |")
        print("|---|---|---|")
        for name in UPDATES:
            r = results[(size, name)]
            print(f"| {name} | {cell(r['rebuilt'])} | {cell(r['kept'])} |")
