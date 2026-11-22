"""Attività 6.1: l'uso ingenuo di e-means rompe l'indice anche con il codice di Faiss?

Il crollo del recall del passo 5 è stato misurato con emeans.py, la nostra riscrittura.
Qui lo stesso aggiornamento è fatto con NumpyEmeans di Faiss 1.16.0, senza toccare
nessuna impostazione: centroidi vecchi come partenza, addestramento sui soli articoli nuovi.

Uso: uv run check_faiss_naive.py > results/check_faiss_naive.md
"""

import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

from emeans import emeans
from exp_real import CHUNK, D, K, N0, REPORT, ROUNDS, SEEDS, load, recall, tenth_score
from exp_warm import assign_all

UPDATES = {
    "mai aggiornare": lambda c, added, seed: c,
    "e-means riscritto a mano (emeans.py)": lambda c, added, seed: emeans(added, K, epochs=1, seed=seed, init=c),
    "e-means di Faiss (NumpyEmeans)": lambda c, added, seed: NumpyEmeans(D, K, nepochs=1, seed=seed).train(
        np.ascontiguousarray(added, dtype=np.float32), init_centroids=c.astype(np.float32))[0].astype(np.float64),
}

if __name__ == "__main__":
    docs, doc_dates, queries, query_dates = load()
    docs64 = docs.astype(np.float64)
    results = {name: {r: [] for r in REPORT} for name in UPDATES}
    for seed in SEEDS:
        start = emeans(docs64[:N0], K, epochs=5, seed=seed)
        start_labels = assign_all(docs64[:N0], start)[0]
        state = {name: (start, start_labels) for name in UPDATES}
        for r in range(1, ROUNDS + 1):
            n = N0 + r * CHUNK
            added = docs64[n - CHUNK : n]
            for name, update in UPDATES.items():
                centroids, labels = state[name]
                centroids = update(centroids, added, 1000 * seed + r)
                state[name] = centroids, np.concatenate([labels, assign_all(added, centroids)[0]])
            if r in REPORT:
                usable = query_dates <= doc_dates[n - 1]
                threshold = tenth_score(docs[:n], queries[usable])
                for name, (centroids, labels) in state.items():
                    results[name][r].append(recall(docs[:n], labels, centroids, queries[usable], threshold).mean())
    print(f"Recall@10 leggendo l'1% dell'indice, mediana [min; max] su {len(SEEDS)} seed. Aggiornamento sui soli articoli nuovi.\n")
    print("| Aggiornamento | " + " | ".join(f"Dopo {r} gir{'o' if r == 1 else 'i'}" for r in REPORT) + " |")
    print("|---|" + "---|" * len(REPORT))
    for name, by_round in results.items():
        cells = [f"{np.median(v):.3f} [{min(v):.3f}; {max(v):.3f}]" for v in by_round.values()]
        print(f"| {name} | " + " | ".join(cells) + " |")
