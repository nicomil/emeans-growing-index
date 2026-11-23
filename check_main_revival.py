"""Su Faiss main: quanto dell'effetto dipende dalla rianimazione dei cluster.

L'aggiornamento ingenuo e quello corretto (massa iniziale, lettura della media mobile),
con le tre impostazioni di unused_threshold: None (predefinita su main: costo di rimozione),
0.1 (per massa, come in Faiss 1.16.0), 0 (nessuna rianimazione).

Uso, con un Python che ha Faiss main: python check_main_revival.py news
"""
import sys

import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

import exp_real
from emeans import emeans
from exp_real import BUDGETS, K, N0, SEEDS, TOP, load, recall, tenth_score
from exp_warm import assign_all

SIZE = 10_000
THRESHOLDS = (None, 0.1, 0)


def naive(tau, centroids, counts, added, seed):
    em = NumpyEmeans(exp_real.D, K, nepochs=1, seed=seed, unused_threshold=tau)
    return em.train(added, init_centroids=centroids.astype(np.float32))[0].astype(np.float64)


def fixed(tau, centroids, counts, added, seed):
    em = NumpyEmeans(exp_real.D, K, nepochs=1, seed=seed, unused_threshold=tau)
    em.begin(len(added), centroids.astype(np.float32))
    em._usage[:] = em.recipe["alpha0"] * counts
    order = np.random.RandomState(seed).permutation(len(added))
    batch = em.recipe["batch_size"]
    for start in range(0, len(added), batch):
        em.update(em.accumulate(added[order[start : start + batch]]))
    return em.current_centroids().astype(np.float64)


if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    docs64 = docs.astype(np.float64)
    n = N0 + SIZE
    arms = {(f.__name__, tau): [] for f in (naive, fixed) for tau in THRESHOLDS}
    for seed in SEEDS:
        start = emeans(docs64[:N0], K, epochs=5, seed=seed)
        counts = np.bincount(assign_all(docs64[:N0], start)[0], minlength=K).astype(np.float64)
        added = np.ascontiguousarray(docs[N0:n])
        usable = query_dates <= doc_dates[n - 1]
        threshold = tenth_score(docs[:n], queries[usable])
        for (name, tau), values in arms.items():
            centroids = globals()[name](tau, start, counts, added, 1000 * seed)
            found = recall(docs[:n], assign_all(docs64[:n], centroids)[0], centroids, queries[usable], threshold)
            values.append(float(found[len(BUDGETS) - 1].mean()) / TOP)
    print(f"Insieme di dati: {corpus}. Un aggiornamento da {SIZE} testi, liste ricostruite.")
    print(f"Recall@{TOP} leggendo l'1% dell'indice, mediana [min; max] su {len(SEEDS)} seed.\n")
    print("| unused_threshold | Uso ingenuo | Con massa iniziale e media mobile |")
    print("|---|---|---|")
    cell = lambda v: f"{np.median(v):.3f} [{min(v):.3f}; {max(v):.3f}]"
    for tau in THRESHOLDS:
        print(f"| {tau} | {cell(arms[('naive', tau)])} | {cell(arms[('fixed', tau)])} |")
