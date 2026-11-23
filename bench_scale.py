"""Tempi del ricalcolo completo a scala grande: e-means contro k-means, implementazioni di Faiss.

Va eseguito da solo, senza altri calcoli in corso sulla macchina.

Sui testi dell'indice finale di exp_scale.py (1.550.000 a scala grande) misura, per e-means a
1, 3, 5, 10 epoche e per k-means a 5, 10, 25 iterazioni: il tempo di addestramento dei centroidi,
il tempo per riassegnare tutti i vettori, e il recall@10 dell'indice che ne risulta. Due
ripetizioni con seed diversi, la seconda in ordine inverso. Prima di ogni misura registra il
carico della macchina. I risultati sono salvati dopo ogni misura.

Uso: uv run bench_scale.py arxiv-full [large|small] > results/bench_scale_arxiv-full.md
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
            rows.append({"metodo": method, "passate": amount, "ripetizione": rep, "carico": load, "addestramento": seconds,
                         "riassegnazione": assign_seconds, "recall 0.001": float(found[0]), "recall 0.01": float(found[1])})
            json.dump({"righe": rows, "faiss": faiss.__version__, "testi": len(docs), "centroidi": k}, open(stem + ".json", "w"), ensure_ascii=False, indent=1)
            print(f"{method} {amount}, ripetizione {rep}: {seconds:.1f} s, recall {found[1]:.3f}", file=sys.stderr, flush=True)

    print(f"Insieme di dati: {corpus}. {len(docs)} testi, {k} centroidi, {d} dimensioni. Faiss {faiss.__version__}, {os.cpu_count()} core.")
    print(f"Media su {REPS} ripetizioni; carico massimo della macchina prima di una misura: {max(r['carico'] for r in rows):.1f}.\n")
    print("| Metodo | Passate sui dati | Addestramento (s) | Riassegnazione (s) | Recall@10, 1% letto | Recall@10, 0,1% letto |")
    print("|---|---|---|---|---|---|")
    for method, amount in CONFIGS:
        mine = [r for r in rows if (r["metodo"], r["passate"]) == (method, amount)]
        mean = lambda key: np.mean([r[key] for r in mine])
        print(f"| {method} | {amount} | {mean('addestramento'):.1f} | {mean('riassegnazione'):.1f} | {mean('recall 0.01'):.3f} | {mean('recall 0.001'):.3f} |")
