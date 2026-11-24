"""Timings of the full rebuild at large scale: e-means against k-means, Faiss implementations.

Must be run on its own, with no other computation running on the machine.

On the texts of the final index of exp_scale.py (1,550,000 at large scale) it measures, for e-means at
1, 3, 5, 10 epochs and for k-means at 5, 10, 25 iterations: the training time of the centroids,
the time to reassign all the vectors, and the recall@10 of the resulting index. Two
repetitions with different seeds, the second in reverse order. Before every measurement it records
the load of the machine. The results are saved after every measurement.

Usage: uv run bench_scale.py arxiv-full [large|small] > results/bench_scale_arxiv-full.md
"""

import json
import os
import sys
import time

import faiss
import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

import exp_real
import exp_scale
from exp_real import TOP, recall

REPS = 2
CONFIGS = [("e-means", e) for e in (1, 3, 5, 10)] + [("k-means", i) for i in (5, 10, 25)]

if __name__ == "__main__":
    corpus = sys.argv[1]
    scale = sys.argv[2] if len(sys.argv) > 2 else "large"
    n0, rounds, chunk, k = exp_scale.SCALES[scale]
    exp_real.K = k
    docs, _, queries, _ = exp_scale.load(corpus, n0 + rounds * chunk)
    d = docs.shape[1]
    threshold = exp_scale.tenth_score(docs, queries)
    stem = f"results/bench_scale_{corpus}" + ("" if scale == "large" else f"_{scale}")
    rows = []
    for rep in range(REPS):
        for method, amount in CONFIGS[:: -1 if rep % 2 else 1]:
            load = os.getloadavg()[0]
            start = time.perf_counter()
            if method == "e-means":
                centroids = NumpyEmeans(d, k, nepochs=amount, seed=rep).train(docs)[0]
            else:
                kmeans = faiss.Kmeans(d, k, niter=amount, seed=rep + 1, max_points_per_centroid=len(docs))
                kmeans.train(docs)
                centroids = kmeans.centroids
            seconds = time.perf_counter() - start
            centroids = np.ascontiguousarray(centroids, dtype=np.float32)
            labels, assign_seconds = exp_scale.timed(exp_scale.assign, docs, centroids)
            found = recall(docs, labels, centroids, queries, threshold).mean(axis=1) / TOP
            rows.append({"method": method, "passes": amount, "repetition": rep, "load": load, "training": seconds,
                         "reassignment": assign_seconds, "recall 0.001": float(found[0]), "recall 0.01": float(found[1])})
            json.dump({"rows": rows, "faiss": faiss.__version__, "texts": len(docs), "centroids": k}, open(stem + ".json", "w"), ensure_ascii=False, indent=1)
            print(f"{method} {amount}, repetition {rep}: {seconds:.1f} s, recall {found[1]:.3f}", file=sys.stderr, flush=True)

    print(f"Dataset: {corpus}. {len(docs)} texts, {k} centroids, {d} dimensions. Faiss {faiss.__version__}, {os.cpu_count()} cores.")
    print(f"Mean over {REPS} repetitions; maximum load of the machine before a measurement: {max(r['load'] for r in rows):.1f}.\n")
    print("| Method | Passes over the data | Training (s) | Reassignment (s) | Recall@10, 1% read | Recall@10, 0.1% read |")
    print("|---|---|---|---|---|---|")
    for method, amount in CONFIGS:
        mine = [r for r in rows if (r["method"], r["passes"]) == (method, amount)]
        mean = lambda key: np.mean([r[key] for r in mine])
        print(f"| {method} | {amount} | {mean('training'):.1f} | {mean('reassignment'):.1f} | {mean('recall 0.01'):.3f} | {mean('recall 0.001'):.3f} |")
