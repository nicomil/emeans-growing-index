"""Passo 3: partenza a caldo di e-means su dati sintetici con deriva controllata.

Scenario. Un insieme "vecchio" è già stato raggruppato. Arrivano punti nuovi da
zone diverse dello spazio, fino a essere una frazione f del totale. Si confronta
come aggiornare i centroidi spendendo una sola passata sui dati aggiornati.

"Una passata" è il costo in più. Le strategie a caldo ereditano le 5 epoche già
spese sui dati vecchi; quella con i centroidi vecchi non costa nulla.

Uso: uv run exp_warm.py
"""

import numpy as np

from emeans import INIT_MASS, assign, batch_law, emeans, mse, step_law

D, K, N_OLD, SEEDS = 32, 256, 50_000, 10
FRACTIONS = (0.05, 0.2, 0.5)


def mixture(rng, n, components, shift, spread=0.7):
    """Miscela di gaussiane sovrapposte.

    Le medie distano tra loro meno del raggio del rumore. Con medie più sparse
    (deviazione 2) i gruppi sono netti, il risultato dipende da quanti restano senza
    centroide e l'errore del riferimento varia del 4-8% da un seed all'altro,
    più delle differenze che si vogliono misurare. Così varia dello 0,4%.
    """
    means = rng.normal(0, spread, (components, D))
    means[:, :8] += shift  # la deriva: i punti nuovi occupano un'altra zona in 8 dimensioni
    return means[rng.integers(0, components, n)] + rng.normal(0, 1, (n, D))


def lazy(x, centroids):
    """Una passata di Lloyd dai centroidi vecchi: assegna, poi media. Stile DeDrift-Lazy."""
    labels, _ = assign_all(x, centroids)
    out = centroids.copy()
    counts = np.bincount(labels, minlength=K)
    sums = np.zeros_like(out)
    np.add.at(sums, labels, x)
    out[counts > 0] = sums[counts > 0] / counts[counts > 0, None]
    return out


def assign_all(x, centroids, chunk=65536):
    parts = [assign(x[i : i + chunk], centroids) for i in range(0, len(x), chunk)]
    return np.concatenate([p[0] for p in parts]), np.concatenate([p[1] for p in parts])


REFERENCE = "da zero, 3 epoche (riferimento)"


def run(fraction, seed):
    """Errore di ogni strategia su un insieme di dati. Chiave: (nome, finalizzazione)."""
    rng = np.random.default_rng(1000 + seed)
    old = mixture(rng, N_OLD, 200, 0.0)
    added = mixture(rng, int(N_OLD * fraction / (1 - fraction)), 40, 1.5)
    x = np.vstack([old, added])
    n = len(x)

    old_centroids = emeans(old, K, epochs=5, seed=seed)
    share = np.bincount(assign_all(old, old_centroids)[0], minlength=K) / N_OLD
    batch = batch_law(n, K, 1, D)
    step = step_law(n, K, 1, batch)
    # Massa a regime di un cluster che riceve solo punti vecchi: in un batch dei dati
    # aggiornati i punti vecchi sono una frazione 1 - f.
    steady = batch * share * (1 - fraction)

    def warm(m, step_factor, finalize):
        return emeans(
            x, K, epochs=1, seed=seed, init=old_centroids, init_mass=np.maximum(m * steady, INIT_MASS),
            alpha0=step * step_factor, finalize=finalize,
        )

    # None: la strategia non ha finalizzazione, oppure è il riferimento (sempre finalizzato).
    arms = {
        ("centroidi vecchi, nessun ricalcolo (0 passate)", None): old_centroids,
        ("una passata di Lloyd dai vecchi", None): lazy(x, old_centroids),
        (REFERENCE, None): emeans(x, K, epochs=3, seed=seed),
    }
    for finalize in (True, False):
        arms[("da zero, 1 epoca", finalize)] = emeans(x, K, epochs=1, seed=seed, finalize=finalize)
        for m, factor in ((0, 1), (1, 1), (10, 1), (100, 1), (1, 0.25), (10, 0.25)):
            name = f"a caldo, massa {m}" + (", passo/4" if factor != 1 else "") + (" (quasi nulla, come Faiss)" if m == 0 else "")
            arms[(name, finalize)] = warm(m, factor, finalize)
    return {key: mse(x, c) for key, c in arms.items()}, f"{fraction:.0%} nuovi (n={n}, B={batch}, passo={step:.2f})"


if __name__ == "__main__":
    columns = {}
    for fraction in FRACTIONS:
        runs = [run(fraction, seed) for seed in range(SEEDS)]
        # Confronto appaiato: l'eccesso si calcola seed per seed, sugli stessi dati.
        columns[runs[0][1]] = {
            key: np.array([100 * (r[0][key] / r[0][(REFERENCE, None)] - 1) for r in runs]) for key in runs[0][0]
        }
    for finalize in (True, False):
        print(f"\n### {'Con' if finalize else 'Senza'} finalizzazione\n")
        print(f"Errore in eccesso rispetto a e-means da zero con 3 epoche, finalizzato: mediana [minimo; massimo] su {SEEDS} seed.\n")
        print("| Strategia | " + " | ".join(columns) + " |")
        print("|---|" + "---|" * len(columns))
        for name, flag in next(iter(columns.values())):
            if flag in (None, finalize) and name != REFERENCE:
                cells = (c[(name, flag)] for c in columns.values())
                print(f"| {name} | " + " | ".join(f"{np.median(v):+.2f}% [{v.min():+.2f}; {v.max():+.2f}]" for v in cells) + " |")
