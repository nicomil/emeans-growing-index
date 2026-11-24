"""Timings of the full rebuild of an index: e-means against classic k-means, Faiss implementations.

Must be run on its own, with no other computation running on the machine.

For every configuration (e-means at 1, 2, 3, 5, 10 epochs; k-means at 3, 5, 10, 12,
15, 20, 25 iterations) it measures the training time of the centroids on the 200,000
texts of the final index, then, outside the measured time: error on the training
texts, error on the held-out texts, recall@10 of the resulting index.
Six repetitions with different seeds, three in one order and three in the reverse
order, so that no method is always first or last. Before every measurement it records
the load of the machine.

What is compared: NumpyEmeans is a Python loop that calls Faiss for the
assignments; faiss.Kmeans is all in C++. At small scales the fixed cost of Python
weighs on e-means. Neither subsamples the data: for k-means the limit of points
per centroid is raised explicitly, e-means has none.

Usage: uv run bench_rebuild.py news > results/bench_rebuild_news.md
"""

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import faiss
import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

from emeans import mse
from exp_real import BUDGETS, K, TOP, load, recall, tenth_score
from exp_warm import assign_all

REPS = 6
CONFIGS = [("e-means", e) for e in (1, 2, 3, 5, 10)] + [("k-means", i) for i in (3, 5, 10, 12, 15, 20, 25)]


def train(method, amount, x, seed):
    """Load of the machine before the measurement, training time and centroids."""
    d = x.shape[1]
    load = os.getloadavg()[0]
    start = time.perf_counter()
    if method == "e-means":
        centroids, _ = NumpyEmeans(d, K, nepochs=amount, seed=seed).train(x)
    else:
        kmeans = faiss.Kmeans(d, K, niter=amount, seed=seed + 1, max_points_per_centroid=len(x))
        kmeans.train(x)
        centroids = kmeans.centroids
    return load, time.perf_counter() - start, np.asarray(centroids, dtype=np.float64)


if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    x = np.ascontiguousarray(docs)
    docs64 = docs.astype(np.float64)
    held = queries[query_dates <= doc_dates[-1]]
    held64 = held.astype(np.float64)
    threshold = tenth_score(docs, held)
    for method in ("e-means", "k-means"):  # warm-up, not measured
        train(method, 1, x[:20_000], 0)
    time.sleep(20)  # lets the load produced by the preparations drop

    records = []
    for rep in range(REPS):
        for method, amount in CONFIGS if rep % 2 == 0 else CONFIGS[::-1]:
            load, seconds, centroids = train(method, amount, x, rep)
            found = recall(docs, assign_all(docs64, centroids)[0], centroids, held, threshold)
            records.append({
                "method": method, "passes": amount, "repetition": rep, "seconds": seconds, "load": load,
                "error": mse(docs64, centroids), "held-out error": mse(held64, centroids),
                **{f"recall {b:.1%}": float(found[i].mean()) / TOP for i, b in enumerate(BUDGETS)},
            })

    chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    print(f"Dataset: {corpus}. {len(docs)} vectors of {docs.shape[1]} dimensions, {K} centroids, {len(held)} held-out texts.")
    print(f"Machine: {chip or platform.processor()}, {platform.platform()}. Faiss {faiss.__version__} with {faiss.omp_get_max_threads()} threads, NumPy {np.__version__}, Python {platform.python_version()}.")
    loads = [r["load"] for r in records]
    print(f"{REPS} repetitions in alternating order. Time: median [minimum; maximum]. The other columns: median.")
    print(f"Load of the machine before the measurements (1-minute average): median {np.median(loads):.1f}, maximum {max(loads):.1f}. "
          "It includes the recall computation of the previous measurement, which uses a single core.\n")
    print("| Method | Passes | Time | Training error | Error on the held-out texts | Recall, 0.1% read | Recall, 1% read |")
    print("|---|---|---|---|---|---|---|")
    for method, amount in CONFIGS:
        rows = [r for r in records if r["method"] == method and r["passes"] == amount]
        med = lambda key: np.median([r[key] for r in rows])
        seconds = [r["seconds"] for r in rows]
        print(
            f"| {method} | {amount} | {np.median(seconds):.1f} s [{min(seconds):.1f}; {max(seconds):.1f}] | {med('error'):.4f} | "
            f"{med('held-out error'):.4f} | {med('recall 0.1%'):.3f} | {med('recall 1.0%'):.3f} |"
        )
    Path(f"results/bench_rebuild_{corpus}.json").write_text(json.dumps(records))
