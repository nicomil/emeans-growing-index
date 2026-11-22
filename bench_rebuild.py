"""Tempi del ricalcolo completo di un indice: e-means contro k-means classico, implementazioni di Faiss.

Va eseguito da solo, senza altri calcoli in corso sulla macchina.

Per ogni configurazione (e-means a 1, 2, 3, 5, 10 epoche; k-means a 3, 5, 10, 12,
15, 20, 25 iterazioni) misura il tempo di addestramento dei centroidi sui 200.000
testi dell'indice finale, poi, fuori dal tempo misurato: errore sui testi di
addestramento, errore sui testi tenuti fuori, recall@10 dell'indice che ne risulta.
Sei ripetizioni con seed diversi, tre in un ordine e tre nell'ordine inverso,
perché nessun metodo sia sempre il primo o l'ultimo. Prima di ogni misura registra
il carico della macchina.

Cosa si confronta: NumpyEmeans è un ciclo in Python che chiama Faiss per le
assegnazioni; faiss.Kmeans è tutto in C++. A scale piccole il costo fisso di Python
pesa su e-means. Nessuno dei due sottocampiona i dati: per k-means il limite di
punti per centroide è alzato esplicitamente, e-means non ne ha.

Uso: uv run bench_rebuild.py news > results/bench_rebuild_news.md
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
    """Carico della macchina prima della misura, tempo di addestramento e centroidi."""
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
    for method in ("e-means", "k-means"):  # riscaldamento, non misurato
        train(method, 1, x[:20_000], 0)
    time.sleep(20)  # lascia scendere il carico prodotto dai preparativi

    records = []
    for rep in range(REPS):
        for method, amount in CONFIGS if rep % 2 == 0 else CONFIGS[::-1]:
            load, seconds, centroids = train(method, amount, x, rep)
            found = recall(docs, assign_all(docs64, centroids)[0], centroids, held, threshold)
            records.append({
                "metodo": method, "passate": amount, "ripetizione": rep, "secondi": seconds, "carico": load,
                "errore": mse(docs64, centroids), "errore fuori": mse(held64, centroids),
                **{f"recall {b:.1%}": float(found[i].mean()) / TOP for i, b in enumerate(BUDGETS)},
            })

    chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    print(f"Insieme di dati: {corpus}. {len(docs)} vettori a {docs.shape[1]} dimensioni, {K} centroidi, {len(held)} testi tenuti fuori.")
    print(f"Macchina: {chip or platform.processor()}, {platform.platform()}. Faiss {faiss.__version__} con {faiss.omp_get_max_threads()} thread, NumPy {np.__version__}, Python {platform.python_version()}.")
    loads = [r["carico"] for r in records]
    print(f"{REPS} ripetizioni in ordine alternato. Tempo: mediana [minimo; massimo]. Le altre colonne: mediana.")
    print(f"Carico della macchina prima delle misure (media a 1 minuto): mediana {np.median(loads):.1f}, massimo {max(loads):.1f}. "
          "Comprende il calcolo del recall della misura precedente, che usa un solo core.\n")
    print("| Metodo | Passate | Tempo | Errore di addestramento | Errore sui testi tenuti fuori | Recall, 0,1% letto | Recall, 1% letto |")
    print("|---|---|---|---|---|---|---|")
    for method, amount in CONFIGS:
        rows = [r for r in records if r["metodo"] == method and r["passate"] == amount]
        med = lambda key: np.median([r[key] for r in rows])
        seconds = [r["secondi"] for r in rows]
        print(
            f"| {method} | {amount} | {np.median(seconds):.1f} s [{min(seconds):.1f}; {max(seconds):.1f}] | {med('errore'):.4f} | "
            f"{med('errore fuori'):.4f} | {med('recall 0.1%'):.3f} | {med('recall 1.0%'):.3f} |"
        )
    Path(f"results/bench_rebuild_{corpus}.json").write_text(json.dumps(records))
