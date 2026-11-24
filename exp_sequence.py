"""Step D: updates in sequence.

Ten updates, one after the other, each with 2,500 new points (5% of the initial
data): the nightly-job scenario. Every strategy restarts from its own centroids of
the previous round.

Two ways of measuring the error:

  lists:      every point stays in the list it was inserted into, as in an IVF
              index that does not reread the vectors already present. If a centroid
              moves, the points of its list do not follow it.
  reassigned: every point is reassigned to the nearest centroid. Requires rereading
              all the vectors after every update.

For the strategies that read only the new points the realistic measure is the first.
The counts used by the strategies are the list sizes.

"Single shot" control: the same update done only once with all 25,000 new points.
If it gives the same error as the ten rounds, the error grows because the shifted
points increase, not because the errors add up from one round to the next.

Three drifts, with the same 40 components in the new zone:
  none:             the new points come from the same distribution as the old ones
  fixed new zone:   all the new points come from the same zone, shifted by 1.5
  zone moving away: the same zone, shifted by a further 0.15 at every round

Usage: uv run exp_sequence.py > results/exp_sequence.md
       (run exp_rule.py overlapping first: it writes the parameters of the rule)
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
SEEDS = range(10, 15)  # datasets never used in the previous steps
DRIFTS = ("none", "fixed new zone", "zone moving away")
SHARE_RULE = json.loads(FIT_FILE.read_text())["from the share"]
REREADS = "warm start on all data, 1 epoch"


def make(rng, drift):
    """Initial data and the new points of every round, of shape (ROUNDS, CHUNK, D)."""
    same = mixture(rng, N_OLD + ROUNDS * CHUNK, 200, 0.0)
    if drift == "none":
        return same[:N_OLD], same[N_OLD:].reshape(ROUNDS, CHUNK, D)
    means = rng.normal(0, 0.7, (40, D))
    new = means[rng.integers(0, 40, (ROUNDS, CHUNK))] + rng.normal(0, 1, (ROUNDS, CHUNK, D))
    shift = np.full(ROUNDS, 1.5) if drift == "fixed new zone" else 1.5 * np.arange(1, ROUNDS + 1) / ROUNDS
    new[:, :, :8] += shift[:, None, None]
    return same[:N_OLD], new


def mass_arm(mass):
    """e-means on the new points only with mass m × step × list size."""
    def update(centroids, counts, added, seen, seed):
        m = mass(len(added) / len(seen)) if callable(mass) else mass
        return warm(added, centroids, counts, m, seed)
    return update


STRATEGIES = {
    "initial centroids, never updated": lambda c, counts, added, seen, seed: c,
    "e-means, near-zero mass and finalization": lambda c, counts, added, seen, seed: emeans(
        added, K, epochs=1, seed=seed, init=c),
    "mini-batch k-means from the list sizes": lambda c, counts, added, seen, seed: online_mean(
        added, c, counts, batch_law(len(added), K, 1, D), seed),
    "e-means, mass 1": mass_arm(1.0),
    "e-means, mass from the share": mass_arm(lambda f: predict(SHARE_RULE, 1.0, f)),
    "e-means, mass 0.2": mass_arm(0.2),
    REREADS: lambda c, counts, added, seen, seed: emeans(seen, K, epochs=1, seed=seed, init=c),
}


def list_mse(x, centroids, labels):
    return float(((x - centroids[labels]) ** 2).sum(1).mean())


def step(name, centroids, labels, added, seen, seed):
    """One update: new centroids and the list of every point seen so far."""
    counts = np.bincount(labels, minlength=K).astype(np.float64)
    centroids = STRATEGIES[name](centroids, counts, added, seen, seed)
    if name == REREADS:  # it rereads everything, so it can reassign everything
        return centroids, assign_all(seen, centroids)[0]
    return centroids, np.concatenate([labels, assign_all(added, centroids)[0]])


def run(drift, seed):
    old, new = make(np.random.default_rng(1000 + seed), drift)
    start = emeans(old, K, epochs=5, seed=seed)
    start_labels = assign_all(old, start)[0]
    start_mse = mse(old, start)
    state = {name: (start, start_labels) for name in STRATEGIES}
    seen = old
    out = {name: {"lists": [], "reassigned": []} for name in STRATEGIES}
    for r in range(1, ROUNDS + 1):
        added = new[r - 1]
        seen = np.vstack([seen, added])
        reference = mse(seen, emeans(seen, K, epochs=10, seed=1000 * seed + r))
        for name in STRATEGIES:
            centroids, labels = state[name] = step(name, *state[name], added, seen, 1000 * seed + r)
            out[name]["lists"].append(100 * (list_mse(seen, centroids, labels) / reference - 1))
            out[name]["reassigned"].append(100 * (mse(seen, centroids) / reference - 1))
    for name in STRATEGIES:
        centroids, labels = state[name]
        # how much the error of the initial points, in their lists, has worsened since the start
        out[name]["initial points"] = 100 * (list_mse(old, centroids, labels[:N_OLD]) / start_mse - 1)
        centroids, labels = step(name, start, start_labels, new.reshape(-1, D), seen, 1000 * seed)
        out[name]["single shot, lists"] = 100 * (list_mse(seen, centroids, labels) / reference - 1)
        out[name]["single shot, reassigned"] = 100 * (mse(seen, centroids) / reference - 1)
    return out


def cell(values, spread=False):
    values = np.asarray(values)
    return f"{np.median(values):+.2f}%" + (f" [{values.min():+.2f}; {values.max():+.2f}]" if spread else "")


if __name__ == "__main__":
    raw = {}
    print(f"{ROUNDS} rounds of {CHUNK} new points on {N_OLD} initial ones; {len(SEEDS)} datasets.\n")
    print(
        "Excess error relative to e-means from scratch on all data, 10 epochs, redone at every round. Median; "
        "where indicated also [minimum; maximum]. The reference sees the new points while it trains: part "
        "of the excess of the never-updated centroids is this, not degradation."
    )
    print(
        f"Reads in {ROUNDS} rounds: {ROUNDS * CHUNK} points for the strategies on the new points only, "
        f"{sum(N_OLD + r * CHUNK for r in range(1, ROUNDS + 1))} for the one that rereads everything."
    )
    for drift in DRIFTS:
        runs = raw[drift] = [run(drift, seed) for seed in SEEDS]
        print(f"\n### Drift: {drift}\n")
        print(
            "| Strategy | Lists, after 1 round | after 5 | after 10 | Lists, single shot | Reassigned, after 10 | "
            "Reassigned, single shot | Initial points in their lists, after 10 |"
        )
        print("|---|" + "---|" * 7)
        for name in STRATEGIES:
            get = lambda key, r=None: [run_[name][key] if r is None else run_[name][key][r - 1] for run_ in runs]
            print(
                f"| {name} | {cell(get('lists', 1))} | {cell(get('lists', 5))} | {cell(get('lists', 10), True)} | "
                f"{cell(get('single shot, lists'))} | {cell(get('reassigned', 10), True)} | "
                f"{cell(get('single shot, reassigned'))} | {cell(get('initial points'))} |"
            )
    Path("results/exp_sequence.json").write_text(json.dumps({"seed": list(SEEDS), "rounds": ROUNDS, "runs": raw}))
