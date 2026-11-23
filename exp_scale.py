"""L'esperimento di exp_real.py portato a scala più grande, con il solo codice di Faiss.

Un indice IVF costruito sui primi testi in ordine di data riceve ROUNDS blocchi di testi
più recenti. Strategie:

  - mai aggiornare i centroidi;
  - e-means di Faiss sui soli testi nuovi, partendo dai centroidi vecchi (uso ingenuo);
  - k-means di Faiss, una iterazione sui soli testi nuovi dai centroidi vecchi;
  - e-means di Faiss con massa iniziale e lettura della media mobile;
  - ricalcolo da zero su tutti i testi, e-means a 3 epoche; a fine corsa anche a 10 (riferimento);
  - DeDrift (Baranchuk e altri, ICCV 2023), riscritto dal testo del paper, sezione 5.1, perché
    non risulta codice pubblicato. Lazy: ogni centroide diventa la media dei vettori della sua
    lista, senza spostare vettori. Split: i vettori delle k liste più grandi e delle k2 - k più
    piccole sono raggruppati di nuovo con k-means in k2 liste, con k2 scelto perché le liste
    nuove abbiano la dimensione mediana; le altre liste non cambiano. Hybrid: Lazy, poi Split.
    Qui k = centroidi / 256 (nel paper 8 con 4.096 centroidi e 64 con 16.384) e un aggiornamento
    a ogni giro. Il paper non dice quante iterazioni di k-means usa Split né come lo inizializza:
    qui 10, con l'inizializzazione casuale di Faiss.

Per le strategie che leggono solo i testi nuovi il recall è misurato in due modi: con i
vettori lasciati nella lista in cui sono entrati, e con le liste ricostruite al momento
della misura. Il recall è quello di exp_real.py: TOP vicini veri trovati leggendo una quota
fissa dell'indice. Di ogni operazione si registra il tempo: addestramento dei centroidi e
riassegnazione di tutti i vettori sono tenuti separati.

Differenze da exp_real.py, per reggere la scala: tutto in singola precisione, assegnazioni
e vicini veri calcolati con IndexFlat di Faiss, indice iniziale addestrato con NumpyEmeans
(5 epoche) invece che con la riscrittura in NumPy.

Uso: uv run exp_scale.py arxiv-full [seed] > results/exp_scale_arxiv-full_seed0.md
     uv run exp_scale.py arxiv 0 small       # stessa scala di exp_real.py, per confronto
"""

import json
import sys
import time
from pathlib import Path

import faiss
import numpy as np
from faiss.contrib.e_means.e_means import NumpyEmeans

import exp_real
from exp_real import BUDGETS, TOP, recall

SCALES = {  # nome: (testi iniziali, giri, testi per giro, centroidi)
    "large": (800_000, 10, 75_000, 16_384),
    "small": (100_000, 10, 10_000, 2_048),
}
N_QUERIES = 3_000
REPORT = (1, 5, 10)

STALE = "mai aggiornare"
NAIVE = "e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo)"
LLOYD = "k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi"
FIXED = "e-means di Faiss con massa iniziale e media mobile"
COLD = "da zero su tutti i testi, e-means 3 epoche"
REFERENCE = "da zero su tutti i testi, e-means 10 epoche (riferimento)"
REBUILT = " + liste ricostruite"
FROM_SCRATCH = ((COLD, 3), (REFERENCE, 10))


def assign(x, centroids):
    """Lista di ogni vettore: il centroide più vicino."""
    index = faiss.IndexFlatL2(centroids.shape[1])
    index.add(centroids)
    return np.concatenate([index.search(x[i : i + 100_000], 1)[1][:, 0] for i in range(0, len(x), 100_000)])


def tenth_score(docs, queries):
    """Somiglianza del TOP-esimo vicino vero. I vettori sono normalizzati: basta il prodotto."""
    index = faiss.IndexFlatIP(docs.shape[1])
    index.add(docs)
    return index.search(queries, TOP)[0][:, -1]


def naive(centroids, counts, added, seed):
    return NumpyEmeans(added.shape[1], len(centroids), nepochs=1, seed=seed).train(added, init_centroids=centroids)[0]


def lloyd(centroids, counts, added, seed):
    kmeans = faiss.Kmeans(added.shape[1], len(centroids), niter=1, seed=seed + 1, max_points_per_centroid=len(added))
    kmeans.train(added, init_centroids=centroids)
    return kmeans.centroids


def fixed(centroids, counts, added, seed):
    em = NumpyEmeans(added.shape[1], len(centroids), nepochs=1, seed=seed)
    em.begin(len(added), centroids)
    em._usage[:] = em.recipe["alpha0"] * counts
    order = np.random.RandomState(seed).permutation(len(added))
    batch = em.recipe["batch_size"]
    for start in range(0, len(added), batch):
        em.update(em.accumulate(added[order[start : start + batch]]))
    return em.current_centroids()


def lazy(centroids, labels, seen, seed):
    """Ogni centroide diventa la media della propria lista; le liste vuote restano dove sono."""
    order = np.argsort(labels, kind="stable")
    sizes = np.bincount(labels, minlength=len(centroids))
    filled = np.flatnonzero(sizes)
    sums = np.add.reduceat(seen[order], (np.cumsum(sizes) - sizes)[filled], axis=0)
    centroids = centroids.copy()
    centroids[filled] = sums / sizes[filled, None]
    return centroids, labels


def split(centroids, labels, seen, seed, niter=10, warm=False):
    """Raggruppa di nuovo le liste più grandi insieme a quante liste piccole servono per non cambiare K.

    Con warm il k-means parte dai centroidi vecchi delle liste coinvolte invece che da punti a caso.
    """
    k = max(1, len(centroids) // 256)
    sizes = np.bincount(labels, minlength=len(centroids))
    by_size = np.argsort(sizes, kind="stable")
    k2 = int(np.ceil(sizes[by_size[-k:]].sum() / np.median(sizes)))
    if k2 <= k:
        return centroids, labels
    involved = np.concatenate([by_size[-k:], by_size[: k2 - k]])
    rows = np.flatnonzero(np.isin(labels, involved))
    kmeans = faiss.Kmeans(seen.shape[1], k2, niter=niter, seed=seed + 1)
    kmeans.train(seen[rows], init_centroids=centroids[involved] if warm else None)
    centroids, labels = centroids.copy(), labels.copy()
    centroids[involved] = kmeans.centroids
    labels[rows] = involved[assign(seen[rows], kmeans.centroids)]
    return centroids, labels


DEDRIFT = {
    "DeDrift-Lazy": lazy,
    "DeDrift-Split": split,
    "DeDrift-Hybrid": lambda c, labels, seen, seed: split(*lazy(c, labels, seen, seed), seen, seed),
}

NEW_ONLY = {STALE: lambda c, counts, added, seed: c, NAIVE: naive, LLOYD: lloyd, FIXED: fixed}


def timed(function, *args):
    start = time.perf_counter()
    out = function(*args)
    return out, time.perf_counter() - start


def load(corpus, n_docs):
    x = np.load(f"data/{corpus}_embeddings.npy", mmap_mode="r")
    dates = np.load(f"data/{corpus}_dates.npy")
    assert len(x) == len(dates) >= n_docs + N_QUERIES
    assert (dates[1:] >= dates[:-1]).all(), "i testi devono essere in ordine di data"
    asked = Path(f"data/{corpus}_queries.npy")
    if asked.exists():  # domande vere di utenti al posto dei testi tenuti fuori
        queries = np.load(asked)[:N_QUERIES]
        return np.ascontiguousarray(x[:n_docs]), dates[:n_docs], queries, np.full(len(queries), dates[n_docs - 1])
    held = np.zeros(len(x), dtype=bool)
    held[np.random.default_rng(0).choice(len(x), N_QUERIES, replace=False)] = True
    kept = np.flatnonzero(~held)[:n_docs]
    return np.ascontiguousarray(x[kept]), dates[kept], np.ascontiguousarray(x[held]), dates[held]


def run(corpus, seed, scale):
    n0, rounds, chunk, k = SCALES[scale]
    exp_real.K = k  # recall() di exp_real legge il numero di liste da lì
    docs, doc_dates, queries, query_dates = load(corpus, n0 + rounds * chunk)
    d = docs.shape[1]
    train = lambda x, epochs, s: np.ascontiguousarray(NumpyEmeans(d, k, nepochs=epochs, seed=s).train(x)[0])
    rows, per_query, times = [], {}, {}
    start, times["indice iniziale: addestramento, 5 epoche"] = timed(train, docs[:n0], 5, seed)
    start_labels, times["indice iniziale: assegnazione"] = timed(assign, docs[:n0], start)
    state = {name: (start, start_labels) for name in (*NEW_ONLY, *DEDRIFT)}
    for r in range(1, rounds + 1):
        n = n0 + r * chunk
        added = docs[n - chunk : n]
        for name, update in NEW_ONLY.items():
            centroids, labels = state[name]
            counts = np.bincount(labels, minlength=k).astype(np.float32)
            centroids, seconds = timed(update, centroids, counts, added, 1000 * seed + r)
            centroids = np.ascontiguousarray(centroids, dtype=np.float32)
            times.setdefault(f"aggiornamento sui nuovi: {name}", []).append(seconds)
            state[name] = centroids, np.concatenate([labels, assign(added, centroids)])
        seen = docs[:n]
        for name, update in DEDRIFT.items():  # i testi nuovi entrano nell'indice, poi l'indice si aggiusta
            centroids, labels = state[name]
            labels = np.concatenate([labels, assign(added, centroids)])
            state[name], seconds = timed(update, centroids, labels, seen, 1000 * seed + r)
            times.setdefault(f"aggiornamento dell'indice: {name}", []).append(seconds)
        if r not in REPORT:
            continue
        indexes = dict(state)
        for name in (NAIVE, LLOYD, FIXED):
            if name not in state:
                continue
            labels, seconds = timed(assign, seen, state[name][0])
            indexes[name + REBUILT] = state[name][0], labels
            times.setdefault("riassegnazione di tutti i vettori", []).append((n, seconds))
        for name, epochs in FROM_SCRATCH:
            if epochs == 10 and r != rounds:
                continue
            centroids, seconds = timed(train, seen, epochs, 1000 * seed + r)
            times.setdefault(f"addestramento: {name}", []).append((n, seconds))
            indexes[name] = centroids, assign(seen, centroids)
        usable = query_dates <= doc_dates[n - 1]
        late = usable & (query_dates > doc_dates[n0 - 1])
        threshold = tenth_score(seen, queries[usable])
        for name, (centroids, labels) in indexes.items():
            found = recall(seen, labels, centroids, queries[usable], threshold)
            per_query[f"{name}|{r}"] = found
            sizes = np.bincount(labels, minlength=k)
            rows.append({
                "giro": r, "testi": n, "strategia": name, "interrogazioni": int(usable.sum()),
                **{f"recall {b}": float(found[i].mean()) / TOP for i, b in enumerate(BUDGETS)},
                "recall 0.01, periodo aggiunto": float(found[-1][late[usable]].mean()) / TOP,
                "sbilanciamento": float(k * (sizes.astype(np.float64) ** 2).sum() / n**2),
            })
            print(f"giro {r}: {name}: {rows[-1]['recall 0.01']:.3f}", file=sys.stderr, flush=True)
    return rows, per_query, times, (n0, rounds, chunk, k, d)


if __name__ == "__main__":
    corpus = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    scale = sys.argv[3] if len(sys.argv) > 3 else "large"
    rows, per_query, times, (n0, rounds, chunk, k, d) = run(corpus, seed, scale)
    main = "_main" if hasattr(faiss, "accumulate_removal_stats") else ""  # funzione presente solo dopo la 1.16.0
    stem = f"results/exp_scale_{corpus}_seed{seed}" + ("" if scale == "large" else f"_{scale}") + main
    json.dump({"righe": rows, "tempi": times, "faiss": faiss.__version__}, open(stem + ".json", "w"), ensure_ascii=False, indent=1)
    np.savez_compressed(stem + ".npz", **per_query)

    print(f"Insieme di dati: {corpus}, seed {seed}. {n0} testi iniziali, {rounds} giri da {chunk}, {k} centroidi, {d} dimensioni.")
    print(f"Faiss {faiss.__version__}{' (ramo principale, compilato dai sorgenti)' if main else ''}. Recall@{TOP}; un solo seed, senza intervalli.\n")
    print("| Strategia | " + " | ".join(f"Giro {r}: 1% letto" for r in REPORT) + f" | Giro {rounds}: periodo aggiunto | Giro {rounds}: 0,1% letto | Sbilanciamento |")
    print("|---|" + "---|" * (len(REPORT) + 3))
    by = {(row["strategia"], row["giro"]): row for row in rows}
    for name in dict.fromkeys(row["strategia"] for row in rows):
        cells = [f"{by[name, r]['recall 0.01']:.3f}" if (name, r) in by else "—" for r in REPORT]
        last = by[name, rounds]
        print(f"| {name} | " + " | ".join(cells) + f" | {last['recall 0.01, periodo aggiunto']:.3f} | {last['recall 0.001']:.3f} | {last['sbilanciamento']:.2f} |")
    print("\nTempi in secondi (misurati dentro l'esperimento: indicativi se la macchina faceva altro).\n")
    print("| Operazione | Tempo |")
    print("|---|---|")
    for name, value in times.items():
        if isinstance(value, float):
            print(f"| {name} | {value:.1f} |")
        elif isinstance(value[0], tuple):
            for n, seconds in dict(value).items():  # per numero di testi: l'ultima misura
                print(f"| {name}, {n} testi | {seconds:.1f} |")
        else:
            print(f"| {name}, mediana su {len(value)} giri | {np.median(value):.1f} |")
