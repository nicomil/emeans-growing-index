"""Passo 4b: scegliere la massa iniziale da un segnale di deriva.

Dal passo 4: leggendo solo i punti nuovi, la massa migliore dipende da quanta
deriva c'è, che in pratica non si conosce. Qui si prova a stimarla da un segnale
che non richiede di rileggere i dati vecchi:

    segnale = errore medio dei punti nuovi sui centroidi vecchi
              / errore medio dei punti vecchi sui centroidi vecchi  −  1

Il denominatore è un numero che l'indice può conservare quando viene costruito.

Leggere il segnale costa una passata in più sui punti nuovi, qui non contata.

Si confrontano quattro regole per la massa m, tarate su alcuni insiemi di dati e
valutate su altri:

    costante:               log m = a
    dal segnale:            log m = a + b · log(segnale)
    dalla quota:            log m = a + c · log(f)        (non usa il segnale)
    dal segnale e dalla quota: log m = a + b · log(segnale) + c · log(f)

Il segnale entra con un minimo di 0,01: senza deriva vale 0,004-0,02, cioè rumore,
e può essere negativo. La massa scelta è limitata all'intervallo della griglia.

Passo fissato a un quarto di quello della legge di scala e rianimazione spenta,
come nella configurazione fissa del passo 4: massa e passo si compensano, quindi
si muove una manopola sola.

Uso: uv run exp_rule.py sovrapposti   (tara le regole e le valuta)
     uv run exp_rule.py netti         (valuta le regole già tarate su dati diversi)
"""

import json
import sys
from pathlib import Path

import numpy as np

from emeans import INIT_MASS, batch_law, emeans, step_law
from exp_new_only import online_mean
from exp_warm import D, K, N_OLD, assign_all, mixture

FRACTIONS = (0.05, 0.2, 0.5)
# nome: (quota dei punti nuovi che viene dalla zona nuova, spostamento della zona)
DRIFTS = {
    "nessuna": (0.0, 0.0),
    "un quarto dei nuovi spostati": (0.25, 1.5),
    "metà dei nuovi spostati": (0.5, 1.5),
    "tutti spostati di poco": (1.0, 0.75),
    "tutti spostati": (1.0, 1.5),
}
MASSES = (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10)
STEP_FACTOR = 0.25
# Gli insiemi 0-4 sono serviti al passo 4 per scegliere passo e rianimazione: la
# valutazione usa insiemi mai visti.
TRAIN_SEEDS, TEST_SEEDS = (0, 1, 2), (5, 6, 7)
# tipo di dati: (dispersione delle medie, moltiplicatore dello spostamento)
SPREADS = {"sovrapposti": (0.7, 1.0), "netti": (2.0, 2.0)}
MODELS = ("costante", "dal segnale", "dalla quota", "dal segnale e dalla quota")
NOISE = 0.05  # punti percentuali: sotto questa soglia una differenza dal mini-batch non conta
FIT_FILE = Path("results/exp_rule_fit.json")


def make(config, fraction, drift, seed):
    """Dati vecchi, punti nuovi, e ciò che l'indice conosce dei vecchi."""
    spread, multiplier = SPREADS[config]
    moved, shift = DRIFTS[drift]
    rng = np.random.default_rng(1000 + seed)
    n_added = int(N_OLD * fraction / (1 - fraction))
    n_moved = round(n_added * moved)
    same = mixture(rng, N_OLD + n_added - n_moved, 200, 0.0, spread)  # stessa distribuzione dei vecchi
    old = same[:N_OLD]
    added = np.vstack([same[N_OLD:], mixture(rng, n_moved, 40, shift * multiplier, spread)])
    added = added[rng.permutation(len(added))]
    centroids = emeans(old, K, epochs=5, seed=seed)
    labels, d2 = assign_all(old, centroids)
    counts = np.bincount(labels, minlength=K).astype(np.float64)
    signal = assign_all(added, centroids)[1].mean() / d2.mean() - 1
    return old, added, centroids, counts, float(signal)


def warm(added, centroids, counts, m, seed):
    k, d = centroids.shape
    batch = batch_law(len(added), k, 1, d)
    alpha0 = min(step_law(len(added), k, 1, batch) * STEP_FACTOR, 1.0)
    return emeans(
        added, k, epochs=1, seed=seed, init=centroids, tau=0, alpha0=alpha0,
        init_mass=np.maximum(m * alpha0 * counts, INIT_MASS), finalize=False,
    )


def total_mse(old, added, centroids):
    return float((assign_all(old, centroids)[1].sum() + assign_all(added, centroids)[1].sum()) / (len(old) + len(added)))


def features(signal, fraction):
    return np.array([1.0, np.log(max(signal, 0.01)), np.log(fraction)])


def predict(params, signal, fraction):
    return float(np.clip(np.exp(np.dot(params, features(signal, fraction))), MASSES[0], MASSES[-1]))


def fit(scenarios):
    """Per ogni regola, i parametri che minimizzano l'errore medio sugli insiemi di taratura.

    scenarios: lista di (segnale, quota, curva), dove curva[j] è l'errore con MASSES[j]
    diviso per quello del mini-batch k-means con conteggi veri. Tra i punti della
    griglia la curva è interpolata. Ricerca esaustiva: i parametri sono al più tre.
    """
    log_masses = np.log(MASSES)
    a = np.linspace(log_masses[0], log_masses[-1], 61)
    b = np.linspace(-2, 1, 61)
    c = np.linspace(-2, 2, 41)
    grids = {
        "costante": np.stack([a, 0 * a, 0 * a], 1),
        "dal segnale": np.stack(np.meshgrid(a, b, [0.0], indexing="ij"), -1).reshape(-1, 3),
        "dalla quota": np.stack(np.meshgrid(a, [0.0], c, indexing="ij"), -1).reshape(-1, 3),
        "dal segnale e dalla quota": np.stack(np.meshgrid(a, b, c, indexing="ij"), -1).reshape(-1, 3),
    }
    fitted = {}
    for model, candidates in grids.items():
        loss = np.zeros(len(candidates))
        for signal, fraction, curve in scenarios:
            predicted = np.clip(candidates @ features(signal, fraction), log_masses[0], log_masses[-1])
            loss += np.interp(predicted, log_masses, curve)
        fitted[model] = candidates[loss.argmin()].tolist()
    return fitted


if __name__ == "__main__":
    config = sys.argv[1] if len(sys.argv) > 1 else "sovrapposti"
    seeds = TRAIN_SEEDS + TEST_SEEDS if config == "sovrapposti" else TEST_SEEDS
    cache = {}  # (quota, deriva, seed) -> dati; errori della griglia
    for fraction in FRACTIONS:
        for drift in DRIFTS:
            for seed in seeds:
                old, added, centroids, counts, signal = data = make(config, fraction, drift, seed)
                batch = batch_law(len(added), K, 1, D)
                cache[(fraction, drift, seed)] = data, {
                    "segnale": signal,
                    "vecchi": total_mse(old, added, centroids),
                    "mini-batch": total_mse(old, added, online_mean(added, centroids, counts, batch, 100 + seed)),
                    "griglia": [total_mse(old, added, warm(added, centroids, counts, m, 100 + seed)) for m in MASSES],
                }

    if config == "sovrapposti":
        scenarios = []
        for fraction in FRACTIONS:
            for drift in DRIFTS:
                runs = [cache[(fraction, drift, seed)][1] for seed in TRAIN_SEEDS]
                curve = np.median([np.array(r["griglia"]) / r["mini-batch"] for r in runs], axis=0)
                scenarios.append((np.median([r["segnale"] for r in runs]), fraction, curve))
        fitted = fit(scenarios)
        FIT_FILE.parent.mkdir(exist_ok=True)
        FIT_FILE.write_text(json.dumps(fitted))
    else:
        fitted = json.loads(FIT_FILE.read_text())

    print(f"## Dati {config}\n")
    print("Regole tarate sui dati sovrapposti, insiemi di dati " + ", ".join(map(str, TRAIN_SEEDS)) + ":\n")
    for model in MODELS:
        a, b, c = fitted[model]
        print(f"- {model}: log m = {a:+.2f} {b:+.2f} · log(segnale) {c:+.2f} · log(f)")
    print(
        f"\nValutazione sugli insiemi di dati {', '.join(map(str, TEST_SEEDS))}. Errore su tutti i dati rispetto al "
        "mini-batch k-means con conteggi veri, mediana: negativo = meglio. L'oracolo è la migliore massa della "
        "griglia scelta guardando il risultato.\n"
    )
    print("| Quota nuovi | Deriva | Segnale | m oracolo | m dal segnale | Centroidi vecchi | Oracolo | " + " | ".join(MODELS) + " |")
    print("|---|---|---|---|---|---|---|" + "---|" * len(MODELS))
    summary = {name: [] for name in ("oracolo",) + MODELS}
    raw = []
    for fraction in FRACTIONS:
        for drift in DRIFTS:
            rows = []
            for seed in TEST_SEEDS:
                (old, added, centroids, counts, signal), r = cache[(fraction, drift, seed)]
                row = {
                    "segnale": signal,
                    "m oracolo": MASSES[int(np.argmin(r["griglia"]))],
                    "m dal segnale": predict(fitted["dal segnale"], signal, fraction),
                    "vecchi": 100 * (r["vecchi"] / r["mini-batch"] - 1),
                    "oracolo": 100 * (min(r["griglia"]) / r["mini-batch"] - 1),
                }
                for model in MODELS:
                    m = predict(fitted[model], signal, fraction)
                    row[model] = 100 * (total_mse(old, added, warm(added, centroids, counts, m, 100 + seed)) / r["mini-batch"] - 1)
                rows.append(row)
            raw.append({"quota": fraction, "deriva": drift, "esecuzioni": rows})
            med = {key: float(np.median([row[key] for row in rows])) for key in rows[0]}
            for name in summary:
                summary[name].append(med[name])
            print(
                f"| {fraction:.0%} | {drift} | {med['segnale']:+.3f} | {med['m oracolo']:g} | {med['m dal segnale']:.2f} | "
                f"{med['vecchi']:+.2f}% | {med['oracolo']:+.2f}% | " + " | ".join(f"{med[m]:+.2f}%" for m in MODELS) + " |"
            )
    print(f"\n| Riepilogo sui 15 casi | Media | Caso peggiore | Casi peggiori del mini-batch di oltre {NOISE} punti |")
    print("|---|---|---|---|")
    for name, values in summary.items():
        print(f"| {name} | {np.mean(values):+.2f}% | {max(values):+.2f}% | {sum(v > NOISE for v in values)} |")
    grids = [{"quota": f, "deriva": d, "seed": seed, **r} for (f, d, seed), (_, r) in cache.items()]
    Path(f"results/exp_rule_{config}.json").write_text(json.dumps({"masse": MASSES, "griglie": grids, "valutazione": raw}))
