Dataset: arxiv-full, seed 0. 800000 initial texts, 10 rounds of 75000, 16384 centroids.
Recall@10 after 10 rounds; a single seed, no intervals.

| Strategy | 1% read | 0.1% read | Imbalance |
|---|---|---|---|
| never update | 0.989 | 0.866 | 1.94 |
| DeDrift-Lazy | 0.990 | 0.877 | 1.83 |
| DeDrift-Split, 10 iterations from random points (as in exp_scale.py) | 0.989 | 0.875 | 1.26 |
| DeDrift-Hybrid, 10 iterations from random points (as in exp_scale.py) | 0.991 | 0.885 | 1.25 |
| DeDrift-Split, 5 iterations from random points | 0.989 | 0.875 | 1.26 |
| DeDrift-Hybrid, 5 iterations from random points | 0.990 | 0.884 | 1.25 |
| DeDrift-Split, 25 iterations from random points | 0.989 | 0.876 | 1.26 |
| DeDrift-Hybrid, 25 iterations from random points | 0.990 | 0.883 | 1.25 |
| DeDrift-Split, 10 iterations from the old centroids | 0.989 | 0.867 | 2.04 |
| DeDrift-Hybrid, 10 iterations from the old centroids | 0.990 | 0.878 | 1.81 |
