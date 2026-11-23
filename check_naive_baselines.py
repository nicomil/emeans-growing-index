"""Quanto del danno dell'uso ingenuo è specifico di e-means, e come cambia con la dimensione dell'aggiornamento?

Un solo aggiornamento di un indice da 100.000 testi, con 10.000 oppure 50.000 testi
nuovi (circa 5 e circa 24 per centroide). I centroidi sono aggiornati leggendo solo
i testi nuovi, in sei modi, tutti con codice di Faiss tranne l'ultimo:

  e-means, train(nuovi, init_centroids=vecchi)       l'uso ingenuo
  e-means sui nuovi, da righe a caso                  senza alcun centroide vecchio
  k-means, una iterazione dai centroidi vecchi        il confronto generico
  e-means con massa iniziale e media mobile           la correzione
  mini-batch k-means dalle dimensioni delle liste     la nostra implementazione

Si misura il recall@10 leggendo l'1% dell'indice, con le liste ricostruite e con le
liste lasciate come sono.

Uso: uv run check_naive_baselines.py news > results/check_naive_baselines_news.md
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
    "mai aggiornare": lambda c, counts, added, seed: c,
    "e-means di Faiss: train(nuovi, init_centroids=vecchi)": faiss_naive,
    "e-means di Faiss sui nuovi, da righe a caso": faiss_scratch,
    "k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi": faiss_lloyd,
    "e-means di Faiss con massa iniziale e media mobile": faiss_fixed,
    "mini-batch k-means dalle dimensioni delle liste": lambda c, counts, added, seed: online_mean(
        added.astype(np.float64), c, counts, batch_law(len(added), K, 1, exp_real.D), seed),
}

if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    docs64 = docs.astype(np.float64)
    one = len(BUDGETS) - 1
    results = {(size, name): {"ricostruite": [], "lasciate": []} for size in SIZES for name in UPDATES}
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
                for key, labels in (("ricostruite", assign_all(docs64[:n], centroids)[0]), ("lasciate", kept)):
                    found = recall(docs[:n], labels, centroids, queries[usable], threshold)
                    results[(size, name)][key].append(float(found[one].mean()) / TOP)
    cell = lambda v: f"{np.median(v):.3f} [{min(v):.3f}; {max(v):.3f}]"
    print(f"Insieme di dati: {corpus}. Un aggiornamento di un indice da {N0} testi, {K} centroidi.")
    print(f"Recall@{TOP} leggendo l'1% dell'indice, mediana [min; max] su {len(SEEDS)} seed.")
    for size in SIZES:
        print(f"\n### {size} testi nuovi (circa {size / K:.0f} per centroide)\n")
        print("| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |")
        print("|---|---|---|")
        for name in UPDATES:
            r = results[(size, name)]
            print(f"| {name} | {cell(r['ricostruite'])} | {cell(r['lasciate'])} |")
