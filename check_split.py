"""How much the two choices the DeDrift paper leaves open weigh on the result.

Split clusters some lists again with k-means, but the paper does not say for how many iterations
nor where it starts from. exp_scale.py uses 10 iterations from random points. Here the same run is
repeated with 5 and 25 iterations and with 10 iterations starting from the old centroids of the
lists involved, for Split and for Hybrid. Everything else is exp_scale.py.

Usage: uv run check_split.py arxiv-full [seed] [large|small] > results/check_split_arxiv-full.md
"""

import sys

import exp_scale
from exp_scale import STALE, lazy, split

VARIANTS = {
    "10 iterations from random points (as in exp_scale.py)": (10, False),
    "5 iterations from random points": (5, False),
    "25 iterations from random points": (25, False),
    "10 iterations from the old centroids": (10, True),
}

if __name__ == "__main__":
    corpus = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    scale = sys.argv[3] if len(sys.argv) > 3 else "large"
    exp_scale.NEW_ONLY = {STALE: exp_scale.NEW_ONLY[STALE]}
    exp_scale.DEDRIFT = {"DeDrift-Lazy": lazy}
    for label, (niter, warm) in VARIANTS.items():
        exp_scale.DEDRIFT[f"DeDrift-Split, {label}"] = lambda c, l, s, r, niter=niter, warm=warm: split(c, l, s, r, niter, warm)
        exp_scale.DEDRIFT[f"DeDrift-Hybrid, {label}"] = lambda c, l, s, r, niter=niter, warm=warm: split(*lazy(c, l, s, r), s, r, niter, warm)
    exp_scale.FROM_SCRATCH = ()
    rounds = exp_scale.SCALES[scale][1]
    exp_scale.REPORT = (rounds,)
    rows, _, _, (n0, rounds, chunk, k, d) = exp_scale.run(corpus, seed, scale)
    print(f"Dataset: {corpus}, seed {seed}. {n0} initial texts, {rounds} rounds of {chunk}, {k} centroids.")
    print(f"Recall@10 after {rounds} rounds; a single seed, no intervals.\n")
    print("| Strategy | 1% read | 0.1% read | Imbalance |")
    print("|---|---|---|---|")
    for row in rows:
        print(f"| {row['strategy']} | {row['recall 0.01']:.3f} | {row['recall 0.001']:.3f} | {row['imbalance']:.2f} |")
