"""Quanto pesano sul risultato le due scelte che il paper di DeDrift non fissa.

Split raggruppa di nuovo alcune liste con k-means, ma il paper non dice per quante iterazioni
né da dove parte. exp_scale.py usa 10 iterazioni da punti a caso. Qui la stessa corsa è ripetuta
con 5 e 25 iterazioni e con 10 iterazioni a partire dai centroidi vecchi delle liste coinvolte,
per Split e per Hybrid. Tutto il resto è exp_scale.py.

Uso: uv run check_split.py arxiv-full [seed] [large|small] > results/check_split_arxiv-full.md
"""

import sys

import exp_scale
from exp_scale import STALE, lazy, split

VARIANTS = {
    "10 iterazioni da punti a caso (come in exp_scale.py)": (10, False),
    "5 iterazioni da punti a caso": (5, False),
    "25 iterazioni da punti a caso": (25, False),
    "10 iterazioni dai centroidi vecchi": (10, True),
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
    print(f"Insieme di dati: {corpus}, seed {seed}. {n0} testi iniziali, {rounds} giri da {chunk}, {k} centroidi.")
    print(f"Recall@10 dopo {rounds} giri; un solo seed, senza intervalli.\n")
    print("| Strategia | 1% letto | 0,1% letto | Sbilanciamento |")
    print("|---|---|---|---|")
    for row in rows:
        print(f"| {row['strategia']} | {row['recall 0.01']:.3f} | {row['recall 0.001']:.3f} | {row['sbilanciamento']:.2f} |")
