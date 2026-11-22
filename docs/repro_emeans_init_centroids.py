"""NumpyEmeans.train(new_rows, init_centroids=old_centroids) behaves like training on new_rows alone.

Self-contained: needs only faiss-cpu >= 1.16.0 and numpy. Runs in under a minute on a laptop.

Scenario: an IVF index was built on `old`. `new` rows arrive from the SAME distribution
(no drift at all). A user refreshes the coarse centroids with one e-means pass over the
new rows, starting from the existing centroids, then rebuilds the inverted lists.

    python repro_emeans_init_centroids.py
"""

import faiss
import numpy as np
from faiss.contrib.e_means import NumpyEmeans

d, k, n_old, n_new, n_query, top, nprobe = 64, 1024, 100_000, 10_000, 2_000, 10, 8
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

    Inverted lists of unequal size make a fixed nprobe scan more vectors, so recall is
    reported at the nprobe whose cost is closest to `target_cost` (or at `nprobe` if None).
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

    if target_cost is None:
        recall, cost = search(nprobe)
    else:
        recall, cost = min((search(p) for p in range(1, 4 * nprobe)), key=lambda rc: abs(rc[1] - target_cost))
    dist, labels = quantizer.search(everything, 1)
    sizes = np.bincount(labels.ravel(), minlength=k)
    return recall, cost, dist.mean(), k * (sizes.astype(float) ** 2).sum() / sizes.sum() ** 2


def emeans(x, epochs, init=None, **kwargs):
    return NumpyEmeans(d, k, nepochs=epochs, seed=0, **kwargs).train(x, init_centroids=init)[0]


c_old = emeans(old, 5)
rows = [
    ("keep the old centroids (no update)", c_old),
    ("retrain from scratch on old + new, 3 epochs", emeans(everything, 3)),
    ("train(new, init_centroids=old centroids), 1 epoch", emeans(new, 1, init=c_old)),
    ("same, with unused_threshold=0 (no revival)", emeans(new, 1, init=c_old, unused_threshold=0)),
    ("train(new) from random rows of new, 1 epoch", emeans(new, 1)),
]
print(f"faiss {faiss.__version__}: d={d}, k={k}, {n_old} old rows, {n_new} new rows from the same distribution")
print(f"IndexIVFFlat over all {len(everything)} rows; recall@{top} at equal search cost (distance computations per query)\n")
_, budget, _, _ = evaluate(c_old)
for name, centroids in rows:
    recall, cost, mse, imbalance = evaluate(centroids, budget)
    print(f"{name:52s} recall {recall:.3f} at {cost:5.0f} dist/query   MSE {mse:6.2f}   imbalance {imbalance:5.2f}")
