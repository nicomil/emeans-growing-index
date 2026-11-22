"""Passi 5 e 6: strategie di aggiornamento di un indice su embedding veri.

L'indice parte dai primi 100.000 testi di un corpus con date e ne riceve altri
100.000 in dieci giri da 10.000, in ordine di data: la deriva è quella vera.

Insiemi di dati (embed_corpus.py): news, arxiv con all-MiniLM-L6-v2 (384 dimensioni);
news-bge, arxiv-bge con bge-base-en-v1.5 (768 dimensioni).

Misure, ai giri riportati:
  errore nelle liste: ogni testo resta nella lista in cui è stato inserito
  recall@10:          per i testi tenuti fuori dall'indice si sondano le liste più
                      vicine fino a leggere esattamente una quota dell'indice (0,1%
                      e 1%); si conta quanti candidati sono vicini almeno quanto il
                      decimo vero, così duplicati e pareggi non contano come errori
Per le strategie sui soli testi nuovi si misura anche cosa succede riassegnando
tutti i vettori ai centroidi aggiornati ("+ liste ricostruite"). La ricostruzione è
fatta una volta sola, al giro riportato, sui centroidi ottenuti senza mai
ricostruire prima: non è la stessa cosa che ricostruire dopo ogni aggiornamento.
Quando il limite di lettura cade dentro una lista, i suoi testi sono letti in
ordine casuale, così i più recenti non sono svantaggiati.

Le interrogazioni sono testi del corpus, non domande di utenti: il recall vale per
"trova testi simili". Si usano solo quelle datate entro il periodo coperto
dall'indice, quindi il loro numero cresce a ogni giro.

Scompone le cause del danno dell'uso ingenuo di e-means (centroidi vecchi come
partenza, addestramento sui soli testi nuovi) accendendo e spegnendo tre cose:
la massa iniziale dei centroidi, la rianimazione dei cluster, le medie finali.
Le tre cose interagiscono: senza massa la rianimazione ricicla centinaia di centroidi
validi, con la massa solo le liste davvero piccole; con le medie finali la massa
conta poco. La tabella va letta per combinazioni, non come somma di tre effetti.

"Massa" ha due unità. Nella scomposizione e nei soli testi nuovi è passo × numero
di testi della lista: il primo aggiornamento equivale alla media con i conteggi veri.
Nelle strategie che rileggono tutto è la massa a regime, batch × quota della lista:
quella che il centroide avrebbe in una corsa già avviata.

Controllo senza deriva: gli stessi testi in ordine casuale, indice mai aggiornato.

I tempi del ricalcolo completo sono in bench_rebuild.py, che va eseguito da solo.

Uso: uv run exp_real.py news > results/exp_real_news.md
"""

import itertools
import json
import sys
from pathlib import Path

import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

from emeans import INIT_MASS, batch_law, emeans, step_law
from exp_new_only import online_mean
from exp_rule import warm
from exp_sequence import list_mse
from exp_warm import assign_all

K = 2048  # 4 · radice di 200.000, arrotondato a potenza di due, come nell'Appendice L del paper
N0, ROUNDS, CHUNK, N_QUERIES = 100_000, 10, 10_000, 3_000
REPORT = (1, 5, 10)
assert REPORT[-1] == ROUNDS
SEEDS = (0, 1, 2)
BUDGETS, TOP = (0.001, 0.01), 10
D = None  # dimensione degli embedding, fissata da load()

STALE = "mai aggiornare"
FAISS_NAIVE = "e-means di Faiss 1.16.0, impostazioni di serie"
ONLINE = "mini-batch k-means dalle dimensioni delle liste"
TUNED = "e-means: massa 0,2, passo/4, senza rianimazione né medie finali"
REFERENCE = "da zero, 10 epoche (riferimento)"
CONTROL = "mai aggiornare, testi in ordine casuale (controllo senza deriva)"
# nome: (epoche, massa a regime, medie finali). Rileggono tutto a ogni giro, ripartendo dai propri centroidi.
WARM = {
    "a caldo, 1 epoca a giro": (1, False, True),
    "a caldo, 3 epoche a giro": (3, False, True),
    "a caldo con massa a regime, 3 epoche a giro": (3, True, True),
    "a caldo con massa a regime, senza medie finali, 3 epoche a giro": (3, True, False),
}
COLD = {"da zero, 1 epoca": 1, "da zero, 3 epoche": 3, REFERENCE: 10}


def ablation_name(mass, revival, closing):
    yes = lambda flag: "sì" if flag else "no"
    return f"e-means: massa {yes(mass)}, rianimazione {yes(revival)}, medie finali {yes(closing)}"


def ablation(mass, revival, closing):
    """e-means sui soli testi nuovi dai centroidi vecchi, con tre interruttori."""
    def update(centroids, counts, added, seed):
        alpha0 = step_law(len(added), K, 1, batch_law(len(added), K, 1, D))
        init_mass = np.maximum(alpha0 * counts, INIT_MASS) if mass else INIT_MASS
        return emeans(added, K, epochs=1, seed=seed, init=centroids, init_mass=init_mass,
                      tau=0.1 if revival else 0.0, finalize=closing)
    return update


def faiss_naive(centroids, counts, added, seed):
    trained, _ = NumpyEmeans(D, K, nepochs=1, seed=seed).train(
        np.ascontiguousarray(added, dtype=np.float32), init_centroids=centroids.astype(np.float32))
    return trained.astype(np.float64)


# nome: aggiornamento(centroidi, dimensioni delle liste, testi nuovi, seed). Leggono solo i testi nuovi.
NEW_ONLY = {
    STALE: lambda c, counts, added, seed: c,
    FAISS_NAIVE: faiss_naive,
    **{ablation_name(*flags): ablation(*flags) for flags in itertools.product((False, True), (True, False), (True, False))},
    ONLINE: lambda c, counts, added, seed: online_mean(added, c, counts, batch_law(len(added), K, 1, D), seed),
    TUNED: lambda c, counts, added, seed: warm(added, c, counts, 0.2, seed),
}


def tenth_score(index, queries):
    """Somiglianza del TOP-esimo testo più vicino a ogni interrogazione. Vettori normalizzati: basta il prodotto."""
    out = []
    for start in range(0, len(queries), 500):
        scores = queries[start : start + 500] @ index.T
        out.append(np.partition(scores, -TOP, axis=1)[:, -TOP])
    return np.concatenate(out)


def recall(index, labels, centroids, queries, threshold, budgets=BUDGETS, nprobe=None):
    """Quanti dei TOP veri si trovano, per ogni interrogazione e per ogni quota dell'indice letta.

    Restituisce interi tra 0 e TOP, di forma (quote, interrogazioni). Con nprobe si
    sondano invece esattamente nprobe liste intere (serve al confronto con Faiss).
    """
    # dentro ogni lista i testi sono in ordine casuale: una lista letta in parte non favorisce i più vecchi
    order = np.lexsort((np.random.default_rng(0).random(len(labels)), labels))
    ends = np.cumsum(np.bincount(labels, minlength=K))
    starts = ends - np.bincount(labels, minlength=K)
    ranking = np.argsort(assign_scores(queries, centroids), axis=1)
    limits = [len(index)] if nprobe else [int(b * len(index)) for b in budgets]
    found = np.zeros((len(limits), len(queries)), dtype=np.uint8)
    for i, query in enumerate(queries):
        candidates, left = [], max(limits)
        for j in ranking[i][:nprobe]:
            members = order[starts[j] : ends[j]][:left]  # l'ultima lista è letta solo in parte
            candidates.append(members)
            left -= len(members)
            if left == 0:
                break
        hits = index[np.concatenate(candidates)] @ query >= threshold[i] - 1e-6
        for b, limit in enumerate(limits):
            found[b, i] = min(int(hits[:limit].sum()), TOP)
    return found


def assign_scores(queries, centroids):
    """Distanza al quadrato da ogni centroide, a meno di una costante per interrogazione."""
    centroids = centroids.astype(np.float32)
    return (centroids**2).sum(1)[None, :] - 2.0 * queries @ centroids.T


def load(corpus="news"):
    global D
    x = np.load(f"data/{corpus}_embeddings.npy")
    dates = np.load(f"data/{corpus}_dates.npy")
    D = x.shape[1]
    assert len(x) == len(dates) >= N0 + ROUNDS * CHUNK + N_QUERIES
    assert (dates[1:] >= dates[:-1]).all(), "i testi devono essere in ordine di data"
    held = np.zeros(len(x), dtype=bool)
    held[np.random.default_rng(0).choice(len(x), N_QUERIES, replace=False)] = True
    docs, doc_dates = x[~held][: N0 + ROUNDS * CHUNK], dates[~held][: N0 + ROUNDS * CHUNK]
    return docs, doc_dates, x[held], dates[held]


def run(seed, docs, doc_dates, queries, query_dates):
    """Restituisce i numeri per strategia e giro, e i risultati interrogazione per interrogazione."""
    docs64 = docs.astype(np.float64)
    old = docs64[:N0]
    start = emeans(old, K, epochs=5, seed=seed)
    start_labels = assign_all(old, start)[0]
    state = {name: (start, start_labels) for name in (*NEW_ONLY, *WARM)}
    out, per_query = {}, {}
    for r in range(1, ROUNDS + 1):
        n = N0 + r * CHUNK
        seen, added = docs64[:n], docs64[n - CHUNK : n]
        for name, update in NEW_ONLY.items():
            centroids, labels = state[name]
            counts = np.bincount(labels, minlength=K).astype(np.float64)
            centroids = update(centroids, counts, added, 1000 * seed + r)
            state[name] = centroids, np.concatenate([labels, assign_all(added, centroids)[0]])
        for name, (epochs, with_mass, closing) in WARM.items():
            centroids, labels = state[name]
            init_mass = INIT_MASS
            if with_mass:  # massa che i centroidi avrebbero in una corsa già a regime
                batch = batch_law(n, K, epochs, D)
                init_mass = np.maximum(batch * np.bincount(labels, minlength=K) / n, INIT_MASS)
            centroids = emeans(seen, K, epochs=epochs, seed=1000 * seed + r, init=centroids, init_mass=init_mass, finalize=closing)
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
            per_query[f"{r}|{name}"] = found
            out.setdefault(name, {})[r] = {
                "errore": 100 * (list_mse(index64, centroids, labels) / reference - 1),
                **{f"recall {b:.1%}": float(found[i].mean()) / TOP for i, b in enumerate(BUDGETS)},
                "recall aggiunto": float(found[-1][recent].mean()) / TOP,
                "interrogazioni": int(usable.sum()),
                "interrogazioni aggiunte": int(recent.sum()),
                "errore assoluto del riferimento": reference,
            }

        for name, (centroids, labels) in indexes.items():
            measure(name, docs[:n], seen, centroids, labels)
            if name in NEW_ONLY and name != STALE:  # e se dopo l'aggiornamento si ricostruissero le liste?
                measure(name + " + liste ricostruite", docs[:n], seen, centroids, assign_all(seen, centroids)[0])
        per_query[f"{r}|recente"] = recent
    # Controllo senza deriva: stessi testi, ordine casuale, centroidi dei primi N0 e mai aggiornati.
    order = np.random.default_rng(seed).permutation(len(docs))
    centroids = emeans(docs64[order[:N0]], K, epochs=5, seed=seed)
    measure(CONTROL, docs[order], docs64[order], centroids, assign_all(docs64[order], centroids)[0])
    out[CONTROL][ROUNDS]["recall aggiunto"] = float("nan")  # in ordine casuale la data non distingue nulla
    return out, per_query


if __name__ == "__main__":
    corpus = sys.argv[1] if len(sys.argv) > 1 else "news"
    docs, doc_dates, queries, query_dates = load(corpus)
    print(f"Insieme di dati: {corpus}, {D} dimensioni.")
    print(f"Indice iniziale: {N0} testi, dal {doc_dates[0]} al {doc_dates[N0 - 1]}.")
    print(f"{ROUNDS} giri da {CHUNK} testi, fino al {doc_dates[-1]}. {K} liste, {len(SEEDS)} seed dell'algoritmo.")
    print(f"Recall@{TOP} leggendo lo 0,1% e l'1% dell'indice. Mediana su {len(SEEDS)} seed. Gli intervalli sono in results/SINTESI.md.\n")
    runs, arrays = [], {}
    for seed in SEEDS:
        out, per_query = run(seed, docs, doc_dates, queries, query_dates)
        runs.append(out)
        arrays.update({f"{seed}|{key}": value for key, value in per_query.items()})
        # si salva dopo ogni seed: un arresto a metà non perde il lavoro fatto
        Path(f"results/exp_real_{corpus}.json").write_text(json.dumps(runs))
        np.savez_compressed(f"results/exp_real_{corpus}.npz", **arrays)
    med = lambda name, r, key: np.median([run_[name][r][key] for run_ in runs])
    for r in REPORT:
        row = runs[0][REFERENCE][r]
        print(
            f"\n### Dopo {r} gir{'o' if r == 1 else 'i'} (indice fino al {doc_dates[N0 + r * CHUNK - 1]}; "
            f"{row['interrogazioni']} interrogazioni, di cui {row['interrogazioni aggiunte']} del periodo aggiunto)\n"
        )
        print("| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |")
        print("|---|---|---|---|---|")
        for name in runs[0]:
            if r in runs[0][name]:
                print(
                    f"| {name} | {med(name, r, 'errore'):+.2f}% | {med(name, r, 'recall 0.1%'):.3f} | "
                    f"{med(name, r, 'recall 1.0%'):.3f} | {'—' if name == CONTROL else format(med(name, r, 'recall aggiunto'), '.3f')} |"
                )
