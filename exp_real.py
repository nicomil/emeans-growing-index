"""Passo 5: gli stessi confronti su embedding veri, con il recall di una ricerca.

Corpus (embed_corpus.py): "news", titoli e sommari HuffPost 2012-2022, oppure
"arxiv", titolo e abstract di articoli arXiv 2007-2021. L'indice parte dai primi
100.000 testi e ne riceve altri 100.000 in dieci giri da 10.000, sempre in ordine
di data: la deriva è quella vera del corpus.

Misure, a ogni giro riportato:
  errore nelle liste: ogni articolo resta nella lista in cui è stato inserito
  recall@10:          per gli articoli tenuti fuori dall'indice si cercano i 10
                      più vicini sondando le liste più prossime fino a leggere
                      l'1% dell'indice esatto; si conta quanti dei candidati sono
                      vicini almeno quanto il decimo vero (così duplicati e
                      pareggi non contano come errori)

Le interrogazioni sono articoli, non domande di utenti: il recall vale per
"trova articoli simili". Si usano solo quelle datate entro il periodo coperto
dall'indice, quindi il loro numero cresce a ogni giro. I giri hanno lo stesso
numero di articoli, non la stessa durata: il corpus si dirada dopo il 2017.

Controllo senza deriva: gli stessi articoli inseriti in ordine casuale in un
indice mai aggiornato. La differenza con l'ordine di data è l'effetto della deriva;
il resto è il costo di centroidi tarati su metà dei dati.

Alla fine confronta anche il ricalcolo completo: e-means a 3 epoche contro
k-means classico a 25, con i tempi delle implementazioni di Faiss.

Uso: uv run --group real embed_corpus.py news      (una volta per corpus)
     uv run exp_real.py news > results/exp_real_news.md
"""

import json
import sys
import time
from pathlib import Path

import faiss
import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

from emeans import batch_law, emeans, mse
from exp_new_only import online_mean
from exp_rule import warm
from exp_sequence import list_mse
from exp_warm import assign_all

K = 2048  # 4 · radice di 200.000, arrotondato a potenza di due, come nell'Appendice L del paper
N0, ROUNDS, CHUNK, N_QUERIES = 100_000, 10, 10_000, 3_000
REPORT = (1, 5, 10)
assert REPORT[-1] == ROUNDS
SEEDS = (0, 1, 2)
SELECTIVITY, TOP = 0.01, 10
REFERENCE = "da zero su tutti i dati, 10 epoche (riferimento)"
CONTROL = "mai aggiornare, articoli in ordine casuale (controllo senza deriva)"
# Strategie che rileggono tutto: nome -> epoche. Quelle a caldo ripartono dai propri centroidi del giro prima.
WARM = {"a caldo su tutti i dati, 1 epoca": 1, "a caldo su tutti i dati, 3 epoche": 3}
COLD = {"da zero su tutti i dati, 1 epoca": 1, "da zero su tutti i dati, 3 epoche": 3, REFERENCE: 10}
D = 384

# nome: aggiornamento(centroidi, dimensioni delle liste, punti nuovi, seed)
NEW_ONLY = {
    "mai aggiornare": lambda c, counts, added, seed: c,
    "e-means, impostazioni di serie (solo nuovi)": lambda c, counts, added, seed: emeans(
        added, K, epochs=1, seed=seed, init=c),
    "mini-batch dalle dimensioni delle liste (solo nuovi)": lambda c, counts, added, seed: online_mean(
        added, c, counts, batch_law(len(added), K, 1, D), seed),
    "e-means, massa 0,2 (solo nuovi)": lambda c, counts, added, seed: warm(added, c, counts, 0.2, seed),
}


def tenth_score(index, queries):
    """Somiglianza del TOP-esimo articolo più vicino a ogni interrogazione. Vettori normalizzati: basta il prodotto."""
    out = []
    for start in range(0, len(queries), 500):
        scores = queries[start : start + 500] @ index.T
        out.append(np.partition(scores, -TOP, axis=1)[:, -TOP])
    return np.concatenate(out)


def recall(index, labels, centroids, queries, threshold):
    """Recall@TOP sondando le liste più vicine fino a leggere esattamente SELECTIVITY dell'indice."""
    order = np.argsort(labels, kind="stable")
    ends = np.cumsum(np.bincount(labels, minlength=K))
    starts = ends - np.bincount(labels, minlength=K)
    ranking = np.argsort(assign_scores(queries, centroids), axis=1)
    found = np.zeros(len(queries))
    for i, query in enumerate(queries):
        candidates, left = [], int(SELECTIVITY * len(index))
        for j in ranking[i]:
            members = order[starts[j] : ends[j]][:left]  # l'ultima lista è letta solo in parte
            candidates.append(members)
            left -= len(members)
            if left == 0:
                break
        scores = index[np.concatenate(candidates)] @ query
        found[i] = min(int((scores >= threshold[i] - 1e-6).sum()), TOP) / TOP
    return found


def assign_scores(queries, centroids):
    """Distanza al quadrato da ogni centroide, a meno di una costante per interrogazione."""
    centroids = centroids.astype(np.float32)
    return (centroids**2).sum(1)[None, :] - 2.0 * queries @ centroids.T


def load(corpus="news"):
    x = np.load(f"data/{corpus}_embeddings.npy")
    dates = np.load(f"data/{corpus}_dates.npy")
    assert x.shape[1] == D and len(x) == len(dates) >= N0 + ROUNDS * CHUNK + N_QUERIES
    assert (dates[1:] >= dates[:-1]).all(), "gli articoli devono essere in ordine di data"
    held = np.zeros(len(x), dtype=bool)
    held[np.random.default_rng(0).choice(len(x), N_QUERIES, replace=False)] = True
    docs, doc_dates = x[~held][: N0 + ROUNDS * CHUNK], dates[~held][: N0 + ROUNDS * CHUNK]
    return docs, doc_dates, x[held], dates[held]


def run(seed, docs, doc_dates, queries, query_dates):
    docs64 = docs.astype(np.float64)
    old = docs64[:N0]
    start = emeans(old, K, epochs=5, seed=seed)
    start_labels = assign_all(old, start)[0]
    state = {name: (start, start_labels) for name in NEW_ONLY}
    state.update({name: (start, start_labels) for name in WARM})
    out = {}
    for r in range(1, ROUNDS + 1):
        n = N0 + r * CHUNK
        seen, added = docs64[:n], docs64[n - CHUNK : n]
        for name, update in NEW_ONLY.items():
            centroids, labels = state[name]
            counts = np.bincount(labels, minlength=K).astype(np.float64)
            centroids = update(centroids, counts, added, 1000 * seed + r)
            state[name] = centroids, np.concatenate([labels, assign_all(added, centroids)[0]])
        for name, epochs in WARM.items():
            centroids = emeans(seen, K, epochs=epochs, seed=1000 * seed + r, init=state[name][0])
            state[name] = centroids, assign_all(seen, centroids)[0]
        if r not in REPORT:
            continue
        indexes = dict(state)
        for name, epochs in COLD.items():
            centroids = emeans(seen, K, epochs=epochs, seed=1000 * seed + r)
            indexes[name] = centroids, assign_all(seen, centroids)[0]
        reference = list_mse(seen, *indexes[REFERENCE])
        # interrogazioni del periodo che l'indice copre, divise tra periodo iniziale e periodo aggiunto
        usable = query_dates <= doc_dates[n - 1]
        recent = query_dates[usable] > doc_dates[N0 - 1]
        threshold = tenth_score(docs[:n], queries[usable])

        def measure(name, index, index64, centroids, labels):
            found = recall(index, labels, centroids, queries[usable], threshold)
            out.setdefault(name, {})[r] = {
                "errore": 100 * (list_mse(index64, centroids, labels) / reference - 1),
                "recall": float(found.mean()),
                "recall iniziale": float(found[~recent].mean()),
                "recall aggiunto": float(found[recent].mean()),
                "interrogazioni": int(usable.sum()),
                "interrogazioni aggiunte": int(recent.sum()),
                "errore assoluto del riferimento": reference,
            }

        for name, (centroids, labels) in indexes.items():
            measure(name, docs[:n], seen, centroids, labels)
    # Controllo senza deriva: stessi articoli, ordine casuale, centroidi dei primi N0 e mai aggiornati.
    order = np.random.default_rng(seed).permutation(len(docs))
    centroids = emeans(docs64[order[:N0]], K, epochs=5, seed=seed)
    measure(CONTROL, docs[order], docs64[order], centroids, assign_all(docs64[order], centroids)[0])
    return out


def full_rebuild(docs, seed):
    """Ricalcolo completo sull'indice finale con le implementazioni di Faiss: tempo ed errore."""
    x = np.ascontiguousarray(docs)
    results = {}
    t = time.perf_counter()
    centroids, _ = NumpyEmeans(D, K, nepochs=3, seed=seed).train(x)
    results["e-means di Faiss, 3 epoche"] = (time.perf_counter() - t, mse(x, centroids))
    for iterations in (3, 5, 10, 25):
        t = time.perf_counter()
        kmeans = faiss.Kmeans(D, K, niter=iterations, seed=seed + 1)
        kmeans.train(x)
        results[f"k-means di Faiss, {iterations} iterazioni"] = (time.perf_counter() - t, mse(x, kmeans.centroids))
    return results


if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    print(f"Corpus: {corpus}.")
    print(f"Indice iniziale: {N0} articoli, dal {doc_dates[0]} al {doc_dates[N0 - 1]}.")
    print(f"{ROUNDS} giri da {CHUNK} articoli, fino al {doc_dates[-1]}. {K} liste, {len(SEEDS)} seed dell'algoritmo, un solo corpus.")
    print(f"Recall@{TOP} leggendo l'{SELECTIVITY:.0%} dell'indice. Mediana su {len(SEEDS)} seed; [min; max] è la sola variabilità dell'algoritmo.")
    print(f"Gli articoli dopo il {doc_dates[-1]} restano fuori dall'esperimento.\n")
    runs = [run(seed, docs, doc_dates, queries, query_dates) for seed in SEEDS]
    med = lambda name, r, key: np.median([run_[name][r][key] for run_ in runs])
    spread = lambda name, r, key: (min(run_[name][r][key] for run_ in runs), max(run_[name][r][key] for run_ in runs))
    for r in REPORT:
        any_row = runs[0][REFERENCE][r]
        print(
            f"\n### Dopo {r} gir{'o' if r == 1 else 'i'} (indice fino al {doc_dates[N0 + r * CHUNK - 1]}; "
            f"{any_row['interrogazioni']} interrogazioni, di cui {any_row['interrogazioni aggiunte']} del periodo aggiunto)\n"
        )
        print("| Strategia | Errore nelle liste | Recall | [min; max] | Recall, periodo iniziale | Recall, periodo aggiunto |")
        print("|---|---|---|---|---|---|")
        for name in runs[0]:
            if r not in runs[0][name]:
                continue
            low, high = spread(name, r, "recall")
            print(
                f"| {name} | {med(name, r, 'errore'):+.2f}% | {med(name, r, 'recall'):.3f} | [{low:.3f}; {high:.3f}] | "
                f"{med(name, r, 'recall iniziale'):.3f} | {med(name, r, 'recall aggiunto'):.3f} |"
            )
    print(f"\n### Ricalcolo completo sull'indice finale, implementazioni di Faiss ({faiss.omp_get_max_threads()} thread)\n")
    print("Una misura per seed, nell'ordine della tabella, nello stesso processo. Errore sui dati di addestramento.\n")
    rebuilds = [full_rebuild(docs, seed) for seed in SEEDS]
    print("| Metodo | Tempo mediano | Errore mediano |")
    print("|---|---|---|")
    for name in rebuilds[0]:
        print(f"| {name} | {np.median([r[name][0] for r in rebuilds]):.1f} s | {np.median([r[name][1] for r in rebuilds]):.4f} |")
    Path(f"results/exp_real_{corpus}.json").write_text(json.dumps({"esecuzioni": runs, "ricalcolo": rebuilds}))
