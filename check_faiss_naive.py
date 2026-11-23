"""L'uso ingenuo di e-means e la sua correzione, fatti con il codice di Faiss.

Il crollo del recall è stato misurato anche con emeans.py, la nostra riscrittura.
Qui lo stesso aggiornamento sui soli testi nuovi è fatto con NumpyEmeans di Faiss 1.16.0:

  ingenuo:  NumpyEmeans.train(nuovi, init_centroids=vecchi), senza toccare nulla;
  corretto: lo stesso passaggio guidato a mano con begin / accumulate / update,
            cambiando due cose: la massa iniziale (passo × numero di testi della
            lista, scritta nell'attributo privato _usage, perché non c'è un modo
            pubblico) e la lettura dei centroidi (current_centroids, cioè la media
            mobile, invece delle medie finali di finalize).

Se la versione corretta con il codice di Faiss dà lo stesso recall della nostra
riscrittura con massa e senza medie finali, la causa è dimostrata dentro Faiss.

Uso: uv run check_faiss_naive.py news > results/check_faiss_naive_news.md
"""

import sys

import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

import exp_real
from emeans import emeans
from exp_real import BUDGETS, CHUNK, K, N0, REPORT, ROUNDS, SEEDS, TOP, ablation, load, recall, tenth_score
from exp_warm import assign_all


def faiss_naive(centroids, counts, added, seed):
    trained, _ = NumpyEmeans(exp_real.D, K, nepochs=1, seed=seed).train(added, init_centroids=centroids.astype(np.float32))
    return trained.astype(np.float64)


def faiss_fixed(centroids, counts, added, seed):
    """Stesso passaggio, con massa iniziale e lettura della media mobile. Solo codice di Faiss."""
    em = NumpyEmeans(exp_real.D, K, nepochs=1, seed=seed)
    em.begin(len(added), centroids.astype(np.float32))
    em._usage[:] = em.recipe["alpha0"] * counts
    order = np.random.RandomState(seed).permutation(len(added))
    batch = em.recipe["batch_size"]
    for start in range(0, len(added), batch):
        em.update(em.accumulate(added[order[start : start + batch]]))
    return em.current_centroids().astype(np.float64)


UPDATES = {
    "mai aggiornare": lambda c, counts, added, seed: c,
    "Faiss, ingenuo: train(nuovi, init_centroids=vecchi)": faiss_naive,
    "Faiss, con massa iniziale e lettura della media mobile": faiss_fixed,
    "nostra riscrittura, ingenuo": ablation(False, True, True),
    "nostra riscrittura, con massa e senza medie finali": ablation(True, True, False),
}

if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    docs64 = docs.astype(np.float64)
    one = len(BUDGETS) - 1
    results = {name: {r: [] for r in REPORT} for name in UPDATES}
    for seed in SEEDS:
        start = emeans(docs64[:N0], K, epochs=5, seed=seed)
        start_labels = assign_all(docs64[:N0], start)[0]
        state = {name: (start, start_labels) for name in UPDATES}
        for r in range(1, ROUNDS + 1):
            n = N0 + r * CHUNK
            for name, update in UPDATES.items():
                centroids, labels = state[name]
                counts = np.bincount(labels, minlength=K).astype(np.float64)
                added = docs64[n - CHUNK : n] if name.startswith(("nostra", "mai")) else np.ascontiguousarray(docs[n - CHUNK : n])
                centroids = update(centroids, counts, added, 1000 * seed + r)
                state[name] = centroids, np.concatenate([labels, assign_all(docs64[n - CHUNK : n], centroids)[0]])
            if r in REPORT:
                usable = query_dates <= doc_dates[n - 1]
                threshold = tenth_score(docs[:n], queries[usable])
                for name, (centroids, labels) in state.items():
                    found = recall(docs[:n], labels, centroids, queries[usable], threshold)
                    results[name][r].append(float(found[one].mean()) / TOP)
    print(f"Insieme di dati: {corpus}. Recall@{TOP} leggendo l'1% dell'indice, liste lasciate come sono, mediana [min; max] su {len(SEEDS)} seed.\n")
    print("| Aggiornamento sui soli testi nuovi | " + " | ".join(f"Dopo {r} gir{'o' if r == 1 else 'i'}" for r in REPORT) + " |")
    print("|---|" + "---|" * len(REPORT))
    for name, by_round in results.items():
        cells = [f"{np.median(v):.3f} [{min(v):.3f}; {max(v):.3f}]" for v in by_round.values()]
        print(f"| {name} | " + " | ".join(cells) + " |")
