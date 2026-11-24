Dataset: arxiv-full, seed 0. 800000 initial texts, 10 rounds of 75000, 16384 centroids, 384 dimensions.
Faiss 1.16.0. Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.989 | 0.989 | 0.989 | 0.988 | 0.866 | 1.94 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.433 | 0.111 | 0.082 | 0.113 | 0.055 | 1.17 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.882 | 0.419 | 0.249 | 0.320 | 0.171 | 1.13 |
| Faiss e-means with initial mass and moving average | 0.989 | 0.990 | 0.990 | 0.989 | 0.879 | 1.77 |
| DeDrift-Lazy | 0.989 | 0.990 | 0.990 | 0.989 | 0.877 | 1.83 |
| DeDrift-Split | 0.989 | 0.989 | 0.989 | 0.989 | 0.875 | 1.26 |
| DeDrift-Hybrid | 0.989 | 0.990 | 0.991 | 0.990 | 0.885 | 1.25 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.911 | 0.933 | 0.944 | 0.951 | 0.607 | 7.13 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.976 | 0.965 | 0.968 | 0.972 | 0.726 | 2.94 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.989 | 0.991 | 0.991 | 0.990 | 0.884 | 1.66 |
| from scratch on all texts, e-means 3 epochs | 0.989 | 0.991 | 0.992 | 0.993 | 0.899 | 1.18 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.993 | 0.993 | 0.903 | 1.16 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 166.5 |
| initial index: assignment | 33.5 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 2.9 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 3.0 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 2.9 |
| index update: DeDrift-Lazy, median over 10 rounds | 2.9 |
| index update: DeDrift-Split, median over 10 rounds | 0.1 |
| index update: DeDrift-Hybrid, median over 10 rounds | 2.6 |
| reassignment of all vectors, 875000 texts | 31.4 |
| reassignment of all vectors, 1175000 texts | 41.8 |
| reassignment of all vectors, 1550000 texts | 55.3 |
| training: from scratch on all texts, e-means 3 epochs, 875000 texts | 101.9 |
| training: from scratch on all texts, e-means 3 epochs, 1175000 texts | 135.7 |
| training: from scratch on all texts, e-means 3 epochs, 1550000 texts | 178.6 |
| training: from scratch on all texts, e-means 10 epochs (reference), 1550000 texts | 594.2 |
