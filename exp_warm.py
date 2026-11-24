"""Step 3: warm start of e-means on synthetic data with controlled drift.

Scenario. An "old" set has already been clustered. New points arrive from
different regions of the space, until they are a fraction f of the total. We compare
ways of updating the centroids by spending a single pass over the updated data.

"One pass" is the extra cost. The warm-start strategies inherit the 5 epochs already
spent on the old data; the one with the old centroids costs nothing.

Usage: uv run exp_warm.py
"""

import numpy as np

from emeans import INIT_MASS, assign, batch_law, emeans, mse, step_law

D, K, N_OLD, SEEDS = 32, 256, 50_000, 10
FRACTIONS = (0.05, 0.2, 0.5)


def mixture(rng, n, components, shift, spread=0.7):
    """Mixture of overlapping Gaussians.

    The means are closer to each other than the radius of the noise. With more
    scattered means (deviation 2) the groups are well separated, the result depends
    on how many are left without a centroid and the error of the reference varies by
    4-8% from one seed to the next, more than the differences to be measured. This
    way it varies by 0.4%.
    """
    means = rng.normal(0, spread, (components, D))
    means[:, :8] += shift  # the drift: the new points occupy another region in 8 dimensions
    return means[rng.integers(0, components, n)] + rng.normal(0, 1, (n, D))


def lazy(x, centroids):
    """One Lloyd pass from the old centroids: assign, then average. DeDrift-Lazy style."""
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


REFERENCE = "from scratch, 3 epochs (reference)"


def run(fraction, seed):
    """Error of every strategy on one dataset. Key: (name, finalization)."""
    rng = np.random.default_rng(1000 + seed)
    old = mixture(rng, N_OLD, 200, 0.0)
    added = mixture(rng, int(N_OLD * fraction / (1 - fraction)), 40, 1.5)
    x = np.vstack([old, added])
    n = len(x)

    old_centroids = emeans(old, K, epochs=5, seed=seed)
    share = np.bincount(assign_all(old, old_centroids)[0], minlength=K) / N_OLD
    batch = batch_law(n, K, 1, D)
    step = step_law(n, K, 1, batch)
    # Steady-state mass of a cluster that receives only old points: in a batch of the
    # updated data the old points are a fraction 1 - f.
    steady = batch * share * (1 - fraction)

    def warm(m, step_factor, finalize):
        return emeans(
            x, K, epochs=1, seed=seed, init=old_centroids, init_mass=np.maximum(m * steady, INIT_MASS),
            alpha0=step * step_factor, finalize=finalize,
        )

    # None: the strategy has no finalization, or it is the reference (always finalized).
    arms = {
        ("old centroids, no recomputation (0 passes)", None): old_centroids,
        ("one Lloyd pass from the old centroids", None): lazy(x, old_centroids),
        (REFERENCE, None): emeans(x, K, epochs=3, seed=seed),
    }
    for finalize in (True, False):
        arms[("from scratch, 1 epoch", finalize)] = emeans(x, K, epochs=1, seed=seed, finalize=finalize)
        for m, factor in ((0, 1), (1, 1), (10, 1), (100, 1), (1, 0.25), (10, 0.25)):
            name = f"warm start, mass {m}" + (", step/4" if factor != 1 else "") + (" (near zero, as in Faiss)" if m == 0 else "")
            arms[(name, finalize)] = warm(m, factor, finalize)
    return {key: mse(x, c) for key, c in arms.items()}, f"{fraction:.0%} new (n={n}, B={batch}, step={step:.2f})"


if __name__ == "__main__":
    columns = {}
    for fraction in FRACTIONS:
        runs = [run(fraction, seed) for seed in range(SEEDS)]
        # Paired comparison: the excess is computed seed by seed, on the same data.
        columns[runs[0][1]] = {
            key: np.array([100 * (r[0][key] / r[0][(REFERENCE, None)] - 1) for r in runs]) for key in runs[0][0]
        }
    for finalize in (True, False):
        print(f"\n### {'With' if finalize else 'Without'} finalization\n")
        print(f"Excess error relative to e-means from scratch with 3 epochs, finalized: median [minimum; maximum] over {SEEDS} seeds.\n")
        print("| Strategy | " + " | ".join(columns) + " |")
        print("|---|" + "---|" * len(columns))
        for name, flag in next(iter(columns.values())):
            if flag in (None, finalize) and name != REFERENCE:
                cells = (c[(name, flag)] for c in columns.values())
                print(f"| {name} | " + " | ".join(f"{np.median(v):+.2f}% [{v.min():+.2f}; {v.max():+.2f}]" for v in cells) + " |")
