"""Step 4: updating the centroids by reading only the new points.

Scenario. The old data are already clustered and we do not want to read them again.
New points arrive, a fraction f of the total. The centroids are updated by reading
only the new points and the error is measured on all the data. Of the old data only
the centroids and how many points each cluster has are assumed known, as in an IVF index.

The knobs of e-means:

  mass m:   initial mass = m × initial step × number of old points in the cluster.
            With a constant and very small step, m = 1 gives the incremental mean in
            which an old point weighs as much as a new one (verified in test_emeans.py).
            With the cosine step of e-means the new points weigh from 1 to 0.1 times
            an old point along the pass, 0.55 on average: m = 1 holds on to the past
            about 1.8 times more than that average.
  step s:   initial step = s × that of the scaling law computed on the new points.
  threshold tau: revival of "dead" clusters. The mass of all clusters is discounted
            at every step, including those that receive no points: an old cluster with
            no new points falls below the threshold and is recycled, even though its
            old points still exist. 0 turns it off.

Usage: uv run exp_new_only.py [overlapping|separated|no-drift]
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
# A single configuration for all columns and all kinds of data. Chosen at the centre
# of the grid after the first run, not retouched per column.
FIXED = dict(m=0.3, s=1 / 4, tau=0.0)
# (spread of the means, shift of the new points). "separated": well-separated groups,
# a regime in which the result depends on how many groups are left without a centroid.
# "no-drift": the new points come from the same mixture as the old ones.
CONFIGS = {"overlapping": (0.7, 1.5), "separated": (2.0, 3.0), "no-drift": (0.7, None)}
STALE = "old centroids, no recomputation"
NAIVE = "e-means, near-zero mass and finalization"
FROZEN = "Lloyd on the new points with frozen old statistics"
ONLINE = "mini-batch k-means with true counts"
EMEANS = "e-means, fixed configuration (m 0.3; s 1/4; no revival)"
REFERENCE = "from scratch on all data, 10 epochs (reference)"


def frozen_lloyd(added, centroids, old_counts, passes):
    """Lloyd on the new points; the old points enter as old centroid × count.

    With one pass it is the incremental mean with the centroids held still during assignment.
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
    """Classic mini-batch k-means (MacQueen, Sculley) starting from the true counts.

    Same batches and same order as emeans with the same seed.
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
    # Key: (name, cost in reads as a multiple of f; None = reads all the data)
    arms = {
        (STALE, 0): old_centroids,
        (NAIVE, 1): emeans(added, K, epochs=1, seed=algo_seed, init=old_centroids),
        (FROZEN, 1): frozen_lloyd(added, old_centroids, old_counts, 1),
        (ONLINE, 1): online_mean(added, old_centroids, old_counts, batch, algo_seed),
        (EMEANS, 1): new_only(**FIXED),
        (FROZEN, 3): frozen_lloyd(added, old_centroids, old_counts, 3),
        (EMEANS, 3): new_only(**FIXED, epochs=3),
        ("warm start on all data, 1 epoch", None): emeans(x, K, epochs=1, seed=algo_seed, init=old_centroids),
        ("from scratch on all data, 1 epoch", None): emeans(x, K, epochs=1, seed=algo_seed),
        (REFERENCE, None): emeans(x, K, epochs=10, seed=algo_seed),
    }
    for tau in TAUS:
        for m in MASSES:
            for s in STEPS:
                arms[(f"grid tau={tau} m={m} s={s}", 1)] = new_only(m, s, tau)
    return {key: split_mse(x, N_OLD, c) for key, c in arms.items()}, (n_added, batch, step_law(n_added, K, 1, batch))


def cell(values):
    return f"{np.median(values):+.2f}% [{values.min():+.2f}; {values.max():+.2f}]"


if __name__ == "__main__":
    config = sys.argv[1] if len(sys.argv) > 1 else "overlapping"
    raw = {}
    print(f"## Data: {config}\n")
    print(
        f"{DATA_SEEDS} datasets × {ALGO_SEEDS} algorithm seeds. The {DATA_SEEDS * ALGO_SEEDS} runs are not "
        "independent: old centroids and strategies without randomness change only with the dataset.\n"
    )
    print("Excess error relative to the reference of the same run: median [minimum; maximum].")
    for fraction in FRACTIONS:
        runs = [run(config, fraction, d, 100 + a) for d in range(DATA_SEEDS) for a in range(ALGO_SEEDS)]
        n_new, batch, step = runs[0][1]
        raw[str(fraction)] = [{f"{name} | {cost}": v for (name, cost), v in r[0].items()} for r in runs]
        # excess[key] has shape (runs, 3): total, old points, new points
        excess = {
            key: np.array([[100 * (r[0][key][i] / r[0][(REFERENCE, None)][i] - 1) for i in range(3)] for r in runs])
            for key in runs[0][0]
        }
        print(f"\n### {fraction:.0%} new points ({n_new} points, batch {batch}, step of the law {step:.3f})\n")
        print("| Strategy | Reads | All data | Old points only | New points only |")
        print("|---|---|---|---|---|")
        for (name, cost), e in excess.items():
            if not name.startswith("grid") and name != REFERENCE:
                reads = "all data" if cost is None else f"{cost * fraction:.2f} × n"
                print(f"| {name} | {reads} | {cell(e[:, 0])} | {np.median(e[:, 1]):+.2f}% | {np.median(e[:, 2]):+.2f}% |")
        print(
            f"\nGrid of e-means, one pass over the new points, without finalization. Median excess on all data; "
            f"in parentheses, in how many runs out of {len(runs)} it beats mini-batch k-means with true counts."
        )
        online = excess[(ONLINE, 1)][:, 0]
        for tau in TAUS:
            print(f"\nRevival {'off' if tau == 0 else f'with threshold {tau}'}:\n")
            print("| mass m | " + " | ".join(f"step ×1/{round(1 / s)}" for s in STEPS) + " |")
            print("|---|" + "---|" * len(STEPS))
            for m in MASSES:
                cells = []
                for s in STEPS:
                    e = excess[(f"grid tau={tau} m={m} s={s}", 1)][:, 0]
                    cells.append(f"{np.median(e):+.2f}% ({int((e < online).sum())})")
                print(f"| {m:g} | " + " | ".join(cells) + " |")
    Path("results").mkdir(exist_ok=True)
    Path(f"results/exp_new_only_{config}.json").write_text(json.dumps(raw))
