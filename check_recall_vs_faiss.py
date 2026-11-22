"""Controllo della misura: il nostro recall coincide con quello di un indice IVF di Faiss?

Il recall degli esperimenti è calcolato da una funzione scritta a mano (exp_real.recall).
Qui si costruisce un vero IndexIVFFlat di Faiss con gli stessi centroidi, vi si
inseriscono gli stessi vettori e si confronta il recall a parità di liste sondate.

Uso: uv run check_recall_vs_faiss.py news > results/check_recall_news.md
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
    index.train(np.ascontiguousarray(docs))  # il quantizzatore ha già i centroidi: non li ricalcola
    index.add(np.ascontiguousarray(docs))
    assert quantizer.ntotal == K

    print(f"Insieme di dati: {corpus}. {len(docs)} vettori, {K} liste, {len(held)} interrogazioni. Recall@{TOP}.\n")
    print("| Liste sondate | Recall con IndexIVFFlat di Faiss | Recall con la nostra funzione | Differenza |")
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
    print(f"\nScarto massimo: {worst:.4f}.")
    assert worst < 0.002, "il nostro recall non coincide con quello di Faiss"
