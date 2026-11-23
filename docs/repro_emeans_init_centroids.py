"""e-means: init_centroids carries no weight, so a pass over new rows forgets the old centroids.

Self-contained: needs only faiss-cpu >= 1.16.0 and numpy.

Scenario: an IVF index was built on `old`. `new` rows arrive from the SAME distribution
(no drift at all). The coarse centroids are refreshed with one pass over the new rows,
starting from the existing centroids, and the inverted lists are rebuilt.

With faiss.Kmeans the starting centroids matter: one Lloyd iteration from them stays close
to the old solution. With NumpyEmeans the result is about as good as starting from random
rows, or from Gaussian noise: the initial centroids get a mass of 2**-16, so the first
batch that touches a centroid replaces it.

    python repro_emeans_init_centroids.py
"""

import faiss
import numpy as np
from faiss.contrib.e_means import NumpyEmeans

d, k, n_old, n_new, n_query, top, nprobe = 64, 2048, 100_000, 10_000, 2_000, 10, 16
rng = np.random.RandomState(0)
means = rng.normal(0, 0.7, (200, d))


def sample(n):
    return (means[rng.randint(0, 200, n)] + rng.normal(0, 1, (n, d))).astype("float32")


old, new, queries = sample(n_old), sample(n_new), sample(n_query)
everything = np.vstack([old, new])
exact = faiss.IndexFlatL2(d)
exact.add(everything)
_, truth = exact.search(queries, top)


def evaluate(centroids, target_cost=None):
    """IndexIVFFlat over all rows: recall@10, distance computations per query, quantization MSE, imbalance.

    Inverted lists of unequal size make a fixed nprobe scan more vectors. Recall is therefore
    reported at the smallest nprobe whose cost reaches `target_cost`, i.e. at a cost equal to
    or above the baseline's, which favours the row being evaluated.
    """
    centroids = np.ascontiguousarray(centroids, dtype="float32")
    quantizer = faiss.IndexFlatL2(d)
    quantizer.add(centroids)
    index = faiss.IndexIVFFlat(quantizer, d, k)
    index.train(everything)  # the quantizer already holds k centroids: nothing is retrained
    index.add(everything)

    def search(probes):
        index.nprobe = probes
        faiss.cvar.indexIVF_stats.reset()
        _, found = index.search(queries, top)
        cost = faiss.cvar.indexIVF_stats.ndis / n_query
        return np.mean([len(np.intersect1d(f, t)) for f, t in zip(found, truth)]) / top, cost

    recall, cost = search(nprobe)
    if target_cost is not None:
        probes = 1
        recall, cost = search(probes)
        while cost < target_cost and probes < k:
            probes += 1
            recall, cost = search(probes)
    dist, labels = quantizer.search(everything, 1)
    sizes = np.bincount(labels.ravel(), minlength=k)
    return recall, cost, dist.mean(), k * (sizes.astype(float) ** 2).sum() / sizes.sum() ** 2


def emeans(x, epochs, init=None, **kwargs):
    return NumpyEmeans(d, k, nepochs=epochs, seed=0, **kwargs).train(x, init_centroids=init)[0]


def emeans_with_usage(x, init, list_sizes):
    """The same single pass, driven by hand so that two things can be changed:
    the initial usage (alpha0 * list size instead of 2**-16) and the read-out
    (the EMA centroids instead of the closing means). `_usage` is private: there
    is no public way to set it."""
    em = NumpyEmeans(d, k, nepochs=1, seed=0)
    em.begin(len(x), init)
    em._usage[:] = em.recipe["alpha0"] * list_sizes
    order = np.random.RandomState(0).permutation(len(x))
    for start in range(0, len(x), em.recipe["batch_size"]):
        em.update(em.accumulate(x[order[start : start + em.recipe["batch_size"]]]))
    return em.current_centroids().copy()


def lloyd(x, iterations, init):
    kmeans = faiss.Kmeans(d, k, niter=iterations, seed=1, max_points_per_centroid=len(x))
    kmeans.train(x, init_centroids=init)
    return kmeans.centroids


c_old = emeans(old, 5)
quantizer_old = faiss.IndexFlatL2(d)
quantizer_old.add(c_old)
sizes_old = np.bincount(quantizer_old.search(old, 1)[1].ravel(), minlength=k)
noise = rng.normal(0, 1, (k, d)).astype("float32")
rows = [
    ("old centroids, not updated", c_old),
    ("from scratch on old + new: e-means, 3 epochs", emeans(everything, 3)),
    ("k-means on new, init = old centroids, 1 iteration", lloyd(new, 1, c_old)),
    ("e-means on new, init = old centroids, 1 epoch", emeans(new, 1, init=c_old)),
    ("  same, unused_threshold=0 (no revival)", emeans(new, 1, init=c_old, unused_threshold=0)),
    ("e-means on new, init = random rows of new, 1 epoch", emeans(new, 1)),
    ("e-means on new, init = Gaussian noise, 1 epoch", emeans(new, 1, init=noise)),
    ("e-means on new, init = old, usage set, EMA read-out", emeans_with_usage(new, c_old, sizes_old)),
]
print(f"faiss {faiss.__version__}: d={d}, k={k}, {n_old} old rows, {n_new} new rows from the same distribution")
print(f"IndexIVFFlat over all {len(everything)} rows; recall@{top} at a search cost >= that of the first row\n")
_, budget, _, _ = evaluate(c_old)
for name, centroids in rows:
    recall, cost, mse, imbalance = evaluate(centroids, budget)
    print(f"{name:52s} recall {recall:.3f} at {cost:5.0f} dist/query   MSE {mse:6.2f}   imbalance {imbalance:5.2f}")
