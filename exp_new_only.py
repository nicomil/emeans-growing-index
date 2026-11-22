"""Passo 4: aggiornare i centroidi leggendo solo i punti nuovi.

Scenario. I dati vecchi sono già raggruppati e non si vogliono rileggere. Arrivano
punti nuovi, una frazione f del totale. Si aggiornano i centroidi leggendo solo i
punti nuovi e si misura l'errore su tutti i dati. Dei dati vecchi si suppongono
noti solo i centroidi e quanti punti ha ogni cluster, come in un indice IVF.

Le manopole di e-means:

  massa m:  massa iniziale = m × passo iniziale × numero di punti vecchi del cluster.
            A passo costante e molto piccolo, m = 1 dà la media incrementale in cui
            un punto vecchio pesa quanto uno nuovo (verificato in test_emeans.py).
            Con il passo a coseno di e-means i punti nuovi pesano da 1 a 0,1 volte
            un punto vecchio lungo la passata, in media 0,55: m = 1 trattiene il
            passato circa 1,8 volte più di quella media.
  passo s:  passo iniziale = s × quello della legge di scala calcolata sui punti nuovi.
  soglia tau: rianimazione dei cluster "morti". La massa di tutti i cluster viene
            scontata a ogni passo, anche di quelli che non ricevono punti: un cluster
            vecchio senza punti nuovi finisce sotto soglia e viene riciclato, benché
            i suoi punti vecchi esistano ancora. 0 la spegne.

Uso: uv run exp_new_only.py [sovrapposti|netti|senza-deriva]
"""

import json
import sys
from pathlib import Path

import numpy as np

from emeans import INIT_MASS, assign, batch_law, emeans, step_law
from exp_warm import D, K, N_OLD, assign_all, mixture

FRACTIONS = (0.05, 0.2, 0.5)
DATA_SEEDS, ALGO_SEEDS = 5, 2
MASSES = (0.03, 0.1, 0.3, 1, 3)
STEPS = (1 / 64, 1 / 16, 1 / 4, 1)
TAUS = (0.1, 0.0)
# Una sola configurazione per tutte le colonne e tutti i tipi di dati. Scelta al centro
# della griglia dopo la prima esecuzione, non ritoccata per colonna.
FIXED = dict(m=0.3, s=1 / 4, tau=0.0)
# (dispersione delle medie, spostamento dei punti nuovi). "netti": gruppi separati,
# regime in cui il risultato dipende da quanti gruppi restano senza centroide.
# "senza-deriva": i punti nuovi vengono dalla stessa miscela dei vecchi.
CONFIGS = {"sovrapposti": (0.7, 1.5), "netti": (2.0, 3.0), "senza-deriva": (0.7, None)}
STALE = "centroidi vecchi, nessun ricalcolo"
NAIVE = "e-means, massa quasi nulla e finalizzazione"
FROZEN = "Lloyd sui nuovi con statistiche vecchie congelate"
ONLINE = "mini-batch k-means con conteggi veri"
EMEANS = "e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione)"
REFERENCE = "da zero su tutti i dati, 10 epoche (riferimento)"


def frozen_lloyd(added, centroids, old_counts, passes):
    """Lloyd sui punti nuovi; i punti vecchi entrano come centroide vecchio × conteggio.

    Con una passata è la media incrementale con i centroidi fermi durante l'assegnazione.
    """
    current = centroids
    for _ in range(passes):
        labels, _ = assign_all(added, current)
        sums = np.zeros_like(centroids)
        np.add.at(sums, labels, added)
        total = old_counts + np.bincount(labels, minlength=K)
        updated = (centroids * old_counts[:, None] + sums) / np.maximum(total, 1)[:, None]
        current = np.where(total[:, None] > 0, updated, centroids)
    return current


def online_mean(added, centroids, old_counts, batch, seed):
    """Mini-batch k-means classico (MacQueen, Sculley) che parte dai conteggi veri.

    Stessi batch e stesso ordine di emeans con lo stesso seed.
    """
    current, counts = centroids.copy(), old_counts.copy()
    order = np.random.default_rng(seed).permutation(len(added))
    for start in range(0, len(added), batch):
        points = added[order[start : start + batch]]
        labels, _ = assign(points, current)
        n = np.bincount(labels, minlength=len(current))
        sums = np.zeros_like(current)
        np.add.at(sums, labels, points)
        hit = n > 0
        counts[hit] += n[hit]
        current[hit] += (sums[hit] - n[hit, None] * current[hit]) / counts[hit, None]
    return current


def split_mse(x, n_old, centroids):
    d2 = assign_all(x, centroids)[1]
    return [float(d2.mean()), float(d2[:n_old].mean()), float(d2[n_old:].mean())]


def run(config, fraction, data_seed, algo_seed):
    spread, shift = CONFIGS[config]
    rng = np.random.default_rng(1000 + data_seed)
    n_added = int(N_OLD * fraction / (1 - fraction))
    if shift is None:
        both = mixture(rng, N_OLD + n_added, 200, 0.0, spread)
        old, added = both[:N_OLD], both[N_OLD:]
    else:
        old = mixture(rng, N_OLD, 200, 0.0, spread)
        added = mixture(rng, n_added, 40, shift, spread)
    x = np.vstack([old, added])

    old_centroids = emeans(old, K, epochs=5, seed=data_seed)
    old_counts = np.bincount(assign_all(old, old_centroids)[0], minlength=K).astype(np.float64)

    def new_only(m, s, tau, epochs=1):
        batch = batch_law(n_added, K, epochs, D)
        alpha0 = min(step_law(n_added, K, epochs, batch) * s, 1.0)
        return emeans(
            added, K, epochs=epochs, seed=algo_seed, init=old_centroids, tau=tau,
            init_mass=np.maximum(m * alpha0 * old_counts, INIT_MASS), alpha0=alpha0, finalize=False,
        )

    batch = batch_law(n_added, K, 1, D)
    # Chiave: (nome, costo in letture come multiplo di f; None = legge tutti i dati)
    arms = {
        (STALE, 0): old_centroids,
        (NAIVE, 1): emeans(added, K, epochs=1, seed=algo_seed, init=old_centroids),
        (FROZEN, 1): frozen_lloyd(added, old_centroids, old_counts, 1),
        (ONLINE, 1): online_mean(added, old_centroids, old_counts, batch, algo_seed),
        (EMEANS, 1): new_only(**FIXED),
        (FROZEN, 3): frozen_lloyd(added, old_centroids, old_counts, 3),
        (EMEANS, 3): new_only(**FIXED, epochs=3),
        ("a caldo su tutti i dati, 1 epoca", None): emeans(x, K, epochs=1, seed=algo_seed, init=old_centroids),
        ("da zero su tutti i dati, 1 epoca", None): emeans(x, K, epochs=1, seed=algo_seed),
        (REFERENCE, None): emeans(x, K, epochs=10, seed=algo_seed),
    }
    for tau in TAUS:
        for m in MASSES:
            for s in STEPS:
                arms[(f"griglia tau={tau} m={m} s={s}", 1)] = new_only(m, s, tau)
    return {key: split_mse(x, N_OLD, c) for key, c in arms.items()}, (n_added, batch, step_law(n_added, K, 1, batch))


def cell(values):
    return f"{np.median(values):+.2f}% [{values.min():+.2f}; {values.max():+.2f}]"


if __name__ == "__main__":
    config = sys.argv[1] if len(sys.argv) > 1 else "sovrapposti"
    raw = {}
    print(f"## Dati {config}\n")
    print(
        f"{DATA_SEEDS} insiemi di dati × {ALGO_SEEDS} seed dell'algoritmo. Le {DATA_SEEDS * ALGO_SEEDS} esecuzioni non sono "
        "indipendenti: centroidi vecchi e strategie senza casualità cambiano solo con l'insieme di dati.\n"
    )
    print("Errore in eccesso rispetto al riferimento della stessa esecuzione: mediana [minimo; massimo].")
    for fraction in FRACTIONS:
        runs = [run(config, fraction, d, 100 + a) for d in range(DATA_SEEDS) for a in range(ALGO_SEEDS)]
        n_new, batch, step = runs[0][1]
        raw[str(fraction)] = [{f"{name} | {cost}": v for (name, cost), v in r[0].items()} for r in runs]
        # eccesso[chiave] ha forma (esecuzioni, 3): totale, punti vecchi, punti nuovi
        excess = {
            key: np.array([[100 * (r[0][key][i] / r[0][(REFERENCE, None)][i] - 1) for i in range(3)] for r in runs])
            for key in runs[0][0]
        }
        print(f"\n### {fraction:.0%} di punti nuovi ({n_new} punti, batch {batch}, passo della legge {step:.3f})\n")
        print("| Strategia | Letture | Tutti i dati | Solo punti vecchi | Solo punti nuovi |")
        print("|---|---|---|---|---|")
        for (name, cost), e in excess.items():
            if not name.startswith("griglia") and name != REFERENCE:
                reads = "tutti i dati" if cost is None else f"{cost * fraction:.2f} × n"
                print(f"| {name} | {reads} | {cell(e[:, 0])} | {np.median(e[:, 1]):+.2f}% | {np.median(e[:, 2]):+.2f}% |")
        print(
            f"\nGriglia di e-means, una passata sui punti nuovi, senza finalizzazione. Eccesso mediano su tutti i dati; "
            f"tra parentesi in quante esecuzioni su {len(runs)} batte il mini-batch k-means con conteggi veri."
        )
        online = excess[(ONLINE, 1)][:, 0]
        for tau in TAUS:
            print(f"\nRianimazione {'spenta' if tau == 0 else f'con soglia {tau}'}:\n")
            print("| massa m | " + " | ".join(f"passo ×1/{round(1 / s)}" for s in STEPS) + " |")
            print("|---|" + "---|" * len(STEPS))
            for m in MASSES:
                cells = []
                for s in STEPS:
                    e = excess[(f"griglia tau={tau} m={m} s={s}", 1)][:, 0]
                    cells.append(f"{np.median(e):+.2f}% ({int((e < online).sum())})")
                print(f"| {m:g} | " + " | ".join(cells) + " |")
    Path("results").mkdir(exist_ok=True)
    Path(f"results/exp_new_only_{config}.json").write_text(json.dumps(raw))
