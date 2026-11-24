"""Step 4b: choosing the initial mass from a drift signal.

From step 4: when only the new points are read, the best mass depends on how much
drift there is, which in practice is unknown. Here we try to estimate it from a
signal that does not require reading the old data again:

    signal = mean error of the new points on the old centroids
             / mean error of the old points on the old centroids  −  1

The denominator is a number the index can store when it is built.

Reading the signal costs one more pass over the new points, not counted here.

Four rules for the mass m are compared, fitted on some datasets and evaluated on
others:

    constant:                      log m = a
    from the signal:               log m = a + b · log(signal)
    from the share:                log m = a + c · log(f)        (does not use the signal)
    from the signal and the share: log m = a + b · log(signal) + c · log(f)

The signal enters with a floor of 0.01: without drift it is 0.004-0.02, i.e. noise,
and it can be negative. The chosen mass is clipped to the range of the grid.

Step fixed at a quarter of that of the scaling law and revival off, as in the
fixed configuration of step 4: mass and step compensate each other, so only one
knob is moved.

Usage: uv run exp_rule.py overlapping   (fits the rules and evaluates them)
       uv run exp_rule.py separated     (evaluates the rules already fitted on different data)
"""

import json
import sys
from pathlib import Path

import numpy as np

from emeans import INIT_MASS, batch_law, emeans, step_law
from exp_new_only import online_mean
from exp_warm import D, K, N_OLD, assign_all, mixture

FRACTIONS = (0.05, 0.2, 0.5)
# name: (share of the new points that comes from the new zone, shift of the zone)
DRIFTS = {
    "none": (0.0, 0.0),
    "a quarter of the new points shifted": (0.25, 1.5),
    "half of the new points shifted": (0.5, 1.5),
    "all shifted slightly": (1.0, 0.75),
    "all shifted": (1.0, 1.5),
}
MASSES = (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10)
STEP_FACTOR = 0.25
# Datasets 0-4 were used in step 4 to choose step and revival: the
# evaluation uses datasets never seen before.
TRAIN_SEEDS, TEST_SEEDS = (0, 1, 2), (5, 6, 7)
# kind of data: (spread of the means, multiplier of the shift)
SPREADS = {"overlapping": (0.7, 1.0), "separated": (2.0, 2.0)}
MODELS = ("constant", "from the signal", "from the share", "from the signal and the share")
NOISE = 0.05  # percentage points: below this threshold a difference from mini-batch does not count
FIT_FILE = Path("results/exp_rule_fit.json")


def make(config, fraction, drift, seed):
    """Old data, new points, and what the index knows about the old ones."""
    spread, multiplier = SPREADS[config]
    moved, shift = DRIFTS[drift]
    rng = np.random.default_rng(1000 + seed)
    n_added = int(N_OLD * fraction / (1 - fraction))
    n_moved = round(n_added * moved)
    same = mixture(rng, N_OLD + n_added - n_moved, 200, 0.0, spread)  # same distribution as the old data
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
    """For every rule, the parameters that minimise the mean error on the fitting datasets.

    scenarios: list of (signal, share, curve), where curve[j] is the error with MASSES[j]
    divided by that of mini-batch k-means with true counts. Between the points of the
    grid the curve is interpolated. Exhaustive search: there are at most three parameters.
    """
    log_masses = np.log(MASSES)
    a = np.linspace(log_masses[0], log_masses[-1], 61)
    b = np.linspace(-2, 1, 61)
    c = np.linspace(-2, 2, 41)
    grids = {
        "constant": np.stack([a, 0 * a, 0 * a], 1),
        "from the signal": np.stack(np.meshgrid(a, b, [0.0], indexing="ij"), -1).reshape(-1, 3),
        "from the share": np.stack(np.meshgrid(a, [0.0], c, indexing="ij"), -1).reshape(-1, 3),
        "from the signal and the share": np.stack(np.meshgrid(a, b, c, indexing="ij"), -1).reshape(-1, 3),
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
    config = sys.argv[1] if len(sys.argv) > 1 else "overlapping"
    seeds = TRAIN_SEEDS + TEST_SEEDS if config == "overlapping" else TEST_SEEDS
    cache = {}  # (share, drift, seed) -> data; errors of the grid
    for fraction in FRACTIONS:
        for drift in DRIFTS:
            for seed in seeds:
                old, added, centroids, counts, signal = data = make(config, fraction, drift, seed)
                batch = batch_law(len(added), K, 1, D)
                cache[(fraction, drift, seed)] = data, {
                    "signal": signal,
                    "old": total_mse(old, added, centroids),
                    "mini-batch": total_mse(old, added, online_mean(added, centroids, counts, batch, 100 + seed)),
                    "grid": [total_mse(old, added, warm(added, centroids, counts, m, 100 + seed)) for m in MASSES],
                }

    if config == "overlapping":
        scenarios = []
        for fraction in FRACTIONS:
            for drift in DRIFTS:
                runs = [cache[(fraction, drift, seed)][1] for seed in TRAIN_SEEDS]
                curve = np.median([np.array(r["grid"]) / r["mini-batch"] for r in runs], axis=0)
                scenarios.append((np.median([r["signal"] for r in runs]), fraction, curve))
        fitted = fit(scenarios)
        FIT_FILE.parent.mkdir(exist_ok=True)
        FIT_FILE.write_text(json.dumps(fitted))
    else:
        fitted = json.loads(FIT_FILE.read_text())

    print(f"## Data: {config}\n")
    print("Rules fitted on the overlapping data, datasets " + ", ".join(map(str, TRAIN_SEEDS)) + ":\n")
    for model in MODELS:
        a, b, c = fitted[model]
        print(f"- {model}: log m = {a:+.2f} {b:+.2f} · log(signal) {c:+.2f} · log(f)")
    print(
        f"\nEvaluation on datasets {', '.join(map(str, TEST_SEEDS))}. Error on all data relative to "
        "mini-batch k-means with true counts, median: negative = better. The oracle is the best mass of the "
        "grid chosen by looking at the result.\n"
    )
    print("| Share of new points | Drift | Signal | oracle m | m from the signal | Old centroids | Oracle | " + " | ".join(MODELS) + " |")
    print("|---|---|---|---|---|---|---|" + "---|" * len(MODELS))
    summary = {name: [] for name in ("oracle",) + MODELS}
    raw = []
    for fraction in FRACTIONS:
        for drift in DRIFTS:
            rows = []
            for seed in TEST_SEEDS:
                (old, added, centroids, counts, signal), r = cache[(fraction, drift, seed)]
                row = {
                    "signal": signal,
                    "oracle m": MASSES[int(np.argmin(r["grid"]))],
                    "m from the signal": predict(fitted["from the signal"], signal, fraction),
                    "old": 100 * (r["old"] / r["mini-batch"] - 1),
                    "oracle": 100 * (min(r["grid"]) / r["mini-batch"] - 1),
                }
                for model in MODELS:
                    m = predict(fitted[model], signal, fraction)
                    row[model] = 100 * (total_mse(old, added, warm(added, centroids, counts, m, 100 + seed)) / r["mini-batch"] - 1)
                rows.append(row)
            raw.append({"share": fraction, "drift": drift, "runs": rows})
            med = {key: float(np.median([row[key] for row in rows])) for key in rows[0]}
            for name in summary:
                summary[name].append(med[name])
            print(
                f"| {fraction:.0%} | {drift} | {med['signal']:+.3f} | {med['oracle m']:g} | {med['m from the signal']:.2f} | "
                f"{med['old']:+.2f}% | {med['oracle']:+.2f}% | " + " | ".join(f"{med[m]:+.2f}%" for m in MODELS) + " |"
            )
    print(f"\n| Summary over the 15 cases | Mean | Worst case | Cases worse than mini-batch by more than {NOISE} points |")
    print("|---|---|---|---|")
    for name, values in summary.items():
        print(f"| {name} | {np.mean(values):+.2f}% | {max(values):+.2f}% | {sum(v > NOISE for v in values)} |")
    grids = [{"share": f, "drift": d, "seed": seed, **r} for (f, d, seed), (_, r) in cache.items()]
    Path(f"results/exp_rule_{config}.json").write_text(json.dumps({"masses": MASSES, "grids": grids, "evaluation": raw}))
