"""Passo D: aggiornamenti in sequenza.

Dieci aggiornamenti, uno dopo l'altro, ciascuno con 2.500 punti nuovi (il 5% dei
dati iniziali): lo scenario del lavoro notturno. Ogni strategia riparte dai propri
centroidi del giro precedente.

Due modi di misurare l'errore:

  liste:        ogni punto resta nella lista in cui è stato inserito, come in un
                indice IVF che non rilegge i vettori già presenti. Se un centroide
                si sposta, i punti della sua lista non lo seguono.
  riassegnando: ogni punto è riassegnato al centroide più vicino. Richiede di
                rileggere tutti i vettori dopo ogni aggiornamento.

Per le strategie che leggono solo i punti nuovi la misura realistica è la prima.
I conteggi usati dalle strategie sono le dimensioni delle liste.

Controllo "colpo unico": lo stesso aggiornamento fatto una volta sola con tutti i
25.000 punti nuovi. Se dà lo stesso errore dei dieci giri, l'errore cresce perché
aumentano i punti spostati, non perché gli errori si sommano da un giro all'altro.

Tre derive, con le stesse 40 componenti nella zona nuova:
  nessuna:               i punti nuovi vengono dalla stessa distribuzione dei vecchi
  zona nuova fissa:      tutti i punti nuovi vengono dalla stessa zona, spostata di 1,5
  zona che si allontana: la stessa zona, spostata di 0,15 in più a ogni giro

Uso: uv run exp_sequence.py > results/exp_sequence.md
     (prima va eseguito exp_rule.py sovrapposti, che scrive i parametri della regola)
"""

import json
from pathlib import Path

import numpy as np

from emeans import batch_law, emeans, mse
from exp_new_only import online_mean
from exp_rule import FIT_FILE, predict, warm
from exp_warm import D, K, N_OLD, assign_all, mixture

ROUNDS, CHUNK = 10, 2_500
REPORT = (1, 5, 10)
assert REPORT[-1] == ROUNDS
SEEDS = range(10, 15)  # insiemi di dati mai usati nei passi precedenti
DRIFTS = ("nessuna", "zona nuova fissa", "zona che si allontana")
QUOTA_RULE = json.loads(FIT_FILE.read_text())["dalla quota"]
REREADS = "a caldo su tutti i dati, 1 epoca"


def make(rng, drift):
    """Dati iniziali e i punti nuovi di ogni giro, di forma (ROUNDS, CHUNK, D)."""
    same = mixture(rng, N_OLD + ROUNDS * CHUNK, 200, 0.0)
    if drift == "nessuna":
        return same[:N_OLD], same[N_OLD:].reshape(ROUNDS, CHUNK, D)
    means = rng.normal(0, 0.7, (40, D))
    new = means[rng.integers(0, 40, (ROUNDS, CHUNK))] + rng.normal(0, 1, (ROUNDS, CHUNK, D))
    shift = np.full(ROUNDS, 1.5) if drift == "zona nuova fissa" else 1.5 * np.arange(1, ROUNDS + 1) / ROUNDS
    new[:, :, :8] += shift[:, None, None]
    return same[:N_OLD], new


def mass_arm(mass):
    """e-means sui soli punti nuovi con massa m × passo × dimensione della lista."""
    def update(centroids, counts, added, seen, seed):
        m = mass(len(added) / len(seen)) if callable(mass) else mass
        return warm(added, centroids, counts, m, seed)
    return update


STRATEGIES = {
    "centroidi iniziali, mai aggiornati": lambda c, counts, added, seen, seed: c,
    "e-means, massa quasi nulla e finalizzazione": lambda c, counts, added, seen, seed: emeans(
        added, K, epochs=1, seed=seed, init=c),
    "mini-batch k-means dalle dimensioni delle liste": lambda c, counts, added, seen, seed: online_mean(
        added, c, counts, batch_law(len(added), K, 1, D), seed),
    "e-means, massa 1": mass_arm(1.0),
    "e-means, massa dalla quota": mass_arm(lambda f: predict(QUOTA_RULE, 1.0, f)),
    "e-means, massa 0,2": mass_arm(0.2),
    REREADS: lambda c, counts, added, seen, seed: emeans(seen, K, epochs=1, seed=seed, init=c),
}


def list_mse(x, centroids, labels):
    return float(((x - centroids[labels]) ** 2).sum(1).mean())


def step(name, centroids, labels, added, seen, seed):
    """Un aggiornamento: centroidi nuovi e lista di ogni punto visto finora."""
    counts = np.bincount(labels, minlength=K).astype(np.float64)
    centroids = STRATEGIES[name](centroids, counts, added, seen, seed)
    if name == REREADS:  # rilegge tutto, quindi può riassegnare tutto
        return centroids, assign_all(seen, centroids)[0]
    return centroids, np.concatenate([labels, assign_all(added, centroids)[0]])


def run(drift, seed):
    old, new = make(np.random.default_rng(1000 + seed), drift)
    start = emeans(old, K, epochs=5, seed=seed)
    start_labels = assign_all(old, start)[0]
    start_mse = mse(old, start)
    state = {name: (start, start_labels) for name in STRATEGIES}
    seen = old
    out = {name: {"liste": [], "riassegnando": []} for name in STRATEGIES}
    for r in range(1, ROUNDS + 1):
        added = new[r - 1]
        seen = np.vstack([seen, added])
        reference = mse(seen, emeans(seen, K, epochs=10, seed=1000 * seed + r))
        for name in STRATEGIES:
            centroids, labels = state[name] = step(name, *state[name], added, seen, 1000 * seed + r)
            out[name]["liste"].append(100 * (list_mse(seen, centroids, labels) / reference - 1))
            out[name]["riassegnando"].append(100 * (mse(seen, centroids) / reference - 1))
    for name in STRATEGIES:
        centroids, labels = state[name]
        # quanto è peggiorato l'errore dei punti iniziali, nelle loro liste, rispetto all'inizio
        out[name]["punti iniziali"] = 100 * (list_mse(old, centroids, labels[:N_OLD]) / start_mse - 1)
        centroids, labels = step(name, start, start_labels, new.reshape(-1, D), seen, 1000 * seed)
        out[name]["colpo unico, liste"] = 100 * (list_mse(seen, centroids, labels) / reference - 1)
        out[name]["colpo unico, riassegnando"] = 100 * (mse(seen, centroids) / reference - 1)
    return out


def cell(values, spread=False):
    values = np.asarray(values)
    return f"{np.median(values):+.2f}%" + (f" [{values.min():+.2f}; {values.max():+.2f}]" if spread else "")


if __name__ == "__main__":
    raw = {}
    print(f"{ROUNDS} giri da {CHUNK} punti nuovi su {N_OLD} iniziali; {len(SEEDS)} insiemi di dati.\n")
    print(
        "Errore in eccesso rispetto a e-means da zero su tutti i dati, 10 epoche, rifatto a ogni giro. Mediana; "
        "dove indicato anche [minimo; massimo]. Il riferimento vede i punti nuovi mentre si addestra: una parte "
        "dell'eccesso dei centroidi mai aggiornati è questo, non degrado."
    )
    print(
        f"Letture in {ROUNDS} giri: {ROUNDS * CHUNK} punti per le strategie sui soli nuovi, "
        f"{sum(N_OLD + r * CHUNK for r in range(1, ROUNDS + 1))} per quella che rilegge tutto."
    )
    for drift in DRIFTS:
        runs = raw[drift] = [run(drift, seed) for seed in SEEDS]
        print(f"\n### Deriva: {drift}\n")
        print(
            "| Strategia | Liste, dopo 1 giro | dopo 5 | dopo 10 | Liste, colpo unico | Riassegnando, dopo 10 | "
            "Riassegnando, colpo unico | Punti iniziali nelle loro liste, dopo 10 |"
        )
        print("|---|" + "---|" * 7)
        for name in STRATEGIES:
            get = lambda key, r=None: [run_[name][key] if r is None else run_[name][key][r - 1] for run_ in runs]
            print(
                f"| {name} | {cell(get('liste', 1))} | {cell(get('liste', 5))} | {cell(get('liste', 10), True)} | "
                f"{cell(get('colpo unico, liste'))} | {cell(get('riassegnando', 10), True)} | "
                f"{cell(get('colpo unico, riassegnando'))} | {cell(get('punti iniziali'))} |"
            )
    Path("results/exp_sequence.json").write_text(json.dumps({"seed": list(SEEDS), "giri": ROUNDS, "esecuzioni": raw}))
