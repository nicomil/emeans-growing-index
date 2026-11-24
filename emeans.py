"""e-means written by hand: mini-batch k-means with an exponential moving average.

Follows Algorithm 1 of "e-means: outperforming k-means (in one-tenth the
epochs)", arXiv 2611.09501. The line numbers in the comments are those of the
algorithm in the paper.

The idea in three sentences. Each centroid has a position c and a mass N, which
says how many points it "remembers". At every batch the centroid moves towards
the mean of the points assigned to it, the more so the more those points weigh
against the mass it had. The old mass is discounted at every step, so the first
batches, seen with centroids that were still wrong, are forgotten.
"""

import math

import numpy as np

INIT_MASS = 1e-10  # line 2: initial mass close to zero, the first batch decides everything
REVIVE_EVERY = 5  # line 9
SPLIT_EPSILON = 1e-4  # how far apart donor and child are placed after a split
ALPHA_MIN_FACTOR = 0.1  # the step decays to one tenth of its initial value

# Coefficients shipped in faiss/contrib/e_means/base.py (Faiss 1.16.0).
# They differ from those in Table 2 of the paper.
_BATCH_LAWS = {  # B = C * k^a * n^b * T^c  (Equation 7)
    "throughput": (0.035134, 0.134749, 0.876473, 0.813344),
    "quality": (0.00439175, 0.134749, 0.876473, 0.813344),
}
_STEP_LAW = (0.8244, -0.4617, 0.9003, -0.4498, -0.1057)  # Equation 6


def batch_law(n, k, epochs, d):
    """Batch size chosen by the scaling law, a power of two."""
    law = "quality" if d <= 16 else "throughput"
    c, a_k, a_n, a_t = _BATCH_LAWS[law]
    batch = 2 ** round(math.log2(c * k**a_k * n**a_n * epochs**a_t))
    cap = n // 2 if law == "quality" else 2 ** round(math.log2(n / 2))
    return max(1, min(batch, cap, n))


def step_law(n, k, epochs, batch):
    """Initial step alpha0: fraction of the way towards the points in one batch."""
    c, a_k, a_b, a_n, a_t = _STEP_LAW
    return min(max(c * k**a_k * batch**a_b * n**a_n * epochs**a_t, 1e-4), 1.0)


def scheduled_alpha(alpha0, step, total_steps):
    """Cosine decay from alpha0 to one tenth of alpha0 (Equation 5)."""
    cosine = 0.5 * (1.0 + math.cos(math.pi * min(step, total_steps) / max(1, total_steps)))
    return alpha0 * (ALPHA_MIN_FACTOR + (1.0 - ALPHA_MIN_FACTOR) * cosine)


def assign(x, centroids):
    """Index of the nearest centroid and squared distance, for every point."""
    # ||x - c||^2 = ||x||^2 - 2 x·c + ||c||^2
    d2 = (x**2).sum(1)[:, None] - 2.0 * x @ centroids.T + (centroids**2).sum(1)[None, :]
    labels = d2.argmin(1)
    return labels, np.maximum(d2[np.arange(len(x)), labels], 0.0)


def revive(centroids, mass, tau, rng):
    """Line 10: nearly empty clusters are reborn by splitting a full cluster in two.

    Modifies centroids and mass in place. Returns how many splits it made.
    """
    dead = mass < tau * mass.mean()
    donors = np.flatnonzero(~dead & (mass > 0))
    targets = np.flatnonzero(dead)
    nsplit = min(len(targets), len(donors))
    if nsplit == 0:
        return 0
    # Donors drawn in proportion to their mass: crowded clusters are split more often.
    source = rng.choice(donors, nsplit, replace=False, p=mass[donors] / mass[donors].sum())
    target = targets[:nsplit]
    sign = np.ones(centroids.shape[1])
    sign[1::2] = -1.0
    offset = SPLIT_EPSILON * sign
    parent = centroids[source]
    # Two almost overlapping copies: the following batches pull them apart.
    centroids[target] = parent * (1.0 + offset)
    centroids[source] = parent * (1.0 - offset)
    # A parent exactly at the origin would give two identical copies that could never be separated.
    same = (centroids[target] == centroids[source]).all(1)
    centroids[target[same], 0] = np.nextafter(centroids[target[same], 0], np.inf)
    mass[target] = mass[source] = mass[source] / 2.0
    return nsplit


def emeans(
    x,
    k,
    epochs=5,
    batch_size=None,
    alpha0=None,
    tau=0.1,
    seed=0,
    on_step=None,
    init=None,
    init_mass=INIT_MASS,
    finalize=True,
):
    """Groups the rows of x into k clusters. Returns the centroids (k, d).

    batch_size and alpha0, when not given, come from the scaling laws.
    tau is the revival threshold; 0 turns revival off.

    Warm start: init holds the centroids to restart from, of shape (k, d), and
    init_mass is how much they weigh, as a single number or as a vector of k values.
    The unit is "points per batch": in steady state the mass of a cluster is about
    batch_size times the share of points that falls to it. With that mass the first
    batch moves the centroid by a fraction alpha, as in a run already under way; with
    the default near-zero mass it replaces the centroid with the batch mean.

    finalize=False skips line 11 and returns the centroids of the moving average.
    Beware: with finalize=True the result is the means of the last epoch, so the
    mass does not limit how far the centroids move. With a huge mass and tau=0 the
    centroids stay still during the epoch and the result is one Lloyd pass.
    on_step(step, centroids, mass, alpha) is called after every update, before
    finalization. It receives the working arrays: copy them if you keep them.
    """
    x = np.asarray(x, dtype=np.float64)
    n, d = x.shape
    if not 1 <= k <= n:
        raise ValueError(f"k must be between 1 and n={n}, got {k}")
    if epochs < 1 or int(epochs) != epochs:
        raise ValueError(f"epochs must be an integer >= 1, got {epochs}")
    if batch_size is None:
        batch_size = batch_law(n, k, epochs, d)
    if alpha0 is None:
        alpha0 = step_law(n, k, epochs, batch_size)
    if batch_size < 1 or not 0 < alpha0 <= 1:
        raise ValueError(f"batch_size >= 1 and 0 < alpha0 <= 1 are required, got {batch_size} and {alpha0}")
    if init is not None and np.shape(init) != (k, d):
        raise ValueError(f"init must have shape {(k, d)}, got {np.shape(init)}")
    rng = np.random.default_rng(seed)
    batch_size = min(batch_size, n)
    starts = range(0, n, batch_size)
    total_steps = epochs * len(starts)

    if init is None:
        centroids = x[rng.choice(n, k, replace=False)].copy()  # line 1
    else:
        centroids = np.array(init, dtype=np.float64)
    mass = np.broadcast_to(np.asarray(init_mass, dtype=np.float64), (k,)).copy()  # line 2
    if not (mass >= 0).all():  # also rejects NaN
        raise ValueError("init_mass cannot be negative")
    step = 0
    for epoch in range(epochs):  # line 3
        order = rng.permutation(n)
        # Counts and sums of the epoch: only needed for finalization (line 11).
        epoch_counts = np.zeros(k)
        epoch_sums = np.zeros((k, d))
        for start in starts:  # line 4
            batch = x[order[start : start + batch_size]]
            alpha = scheduled_alpha(alpha0, step, total_steps)  # line 5
            labels, _ = assign(batch, centroids)  # line 6
            counts = np.bincount(labels, minlength=k).astype(np.float64)  # line 7
            sums = np.zeros((k, d))
            np.add.at(sums, labels, batch)
            epoch_counts += counts
            epoch_sums += sums

            # Line 8. The paper writes N <- gamma N + alpha n, S <- gamma S + alpha s
            # with gamma = 1 - alpha and c = S / N. Here the same thing is written on c and N,
            # so that a cluster with no points stays still even when alpha is 1.
            mass *= 1.0 - alpha
            hit = counts > 0
            new_mass = mass[hit] + alpha * counts[hit]
            weight = alpha * counts[hit] / new_mass  # how much the batch counts against the past
            batch_mean = sums[hit] / counts[hit, None]
            centroids[hit] += weight[:, None] * (batch_mean - centroids[hit])
            mass[hit] = new_mass

            step += 1
            # Line 9. As in Faiss, the epoch sums are not corrected after a split.
            if tau > 0 and step % REVIVE_EVERY == 0:
                revive(centroids, mass, tau, rng)
            if on_step is not None:
                on_step(step, centroids, mass, alpha)

    if finalize:
        # Line 11: plain mean of the points assigned during the last epoch.
        seen = epoch_counts > 0
        centroids[seen] = epoch_sums[seen] / epoch_counts[seen, None]
    return centroids


def mse(x, centroids):
    """Mean squared distance between every point and its centroid."""
    x = np.asarray(x, dtype=np.float64)
    # In blocks: the full distance matrix would take 8 * n * k bytes.
    return float(sum(assign(x[i : i + 65536], centroids)[1].sum() for i in range(0, len(x), 65536)) / len(x))
