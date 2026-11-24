"""Check of the measure: does our recall match that of a Faiss IVF index?

The recall of the experiments is computed by a hand-written function (exp_real.recall).
Here a real Faiss IndexIVFFlat is built with the same centroids, the same vectors are
inserted into it and the recall is compared at an equal number of probed lists.

Usage: uv run check_recall_vs_faiss.py news > results/check_recall_news.md
"""

import sys

import faiss
import numpy as np

from emeans import emeans
from exp_real import K, TOP, load, recall, tenth_score
from exp_warm import assign_all

if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    held = np.ascontiguousarray(queries[query_dates <= doc_dates[-1]])
    docs64 = docs.astype(np.float64)
    centroids = emeans(docs64, K, epochs=3, seed=0)
    labels = assign_all(docs64, centroids)[0]
    threshold = tenth_score(docs, held)

    d = docs.shape[1]
    quantizer = faiss.IndexFlatL2(d)
    quantizer.add(np.ascontiguousarray(centroids, dtype=np.float32))
    index = faiss.IndexIVFFlat(quantizer, d, K)
    index.train(np.ascontiguousarray(docs))  # the quantizer already holds the centroids: it does not recompute them
    index.add(np.ascontiguousarray(docs))
    assert quantizer.ntotal == K

    print(f"Dataset: {corpus}. {len(docs)} vectors, {K} lists, {len(held)} queries. Recall@{TOP}.\n")
    print("| Lists probed | Recall with Faiss IndexIVFFlat | Recall with our function | Difference |")
    print("|---|---|---|---|")
    worst = 0.0
    for nprobe in (1, 4, 16, 64):
        index.nprobe = nprobe
        _, ids = index.search(held, TOP)
        hits = [(docs[row[row >= 0]] @ query >= limit - 1e-6).sum() for row, query, limit in zip(ids, held, threshold)]
        theirs = float(np.mean(hits)) / TOP
        ours = float(recall(docs, labels, centroids, held, threshold, nprobe=nprobe)[0].mean()) / TOP
        worst = max(worst, abs(theirs - ours))
        print(f"| {nprobe} | {theirs:.4f} | {ours:.4f} | {ours - theirs:+.4f} |")
    print(f"\nMaximum gap: {worst:.4f}.")
    assert worst < 0.002, "our recall does not match that of Faiss"
