Dataset: arxiv-full, seed 0. 800000 initial texts, 10 rounds of 75000, 16384 centroids, 384 dimensions.
Faiss 1.16.0 (main branch, built from source). Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.990 | 0.990 | 0.989 | 0.988 | 0.870 | 1.82 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.270 | 0.084 | 0.067 | 0.090 | 0.049 | 1.09 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.885 | 0.410 | 0.249 | 0.314 | 0.173 | 1.12 |
| Faiss e-means with initial mass and moving average | 0.454 | 0.122 | 0.091 | 0.122 | 0.068 | 1.07 |
| DeDrift-Lazy | 0.990 | 0.990 | 0.991 | 0.990 | 0.882 | 1.72 |
| DeDrift-Split | 0.990 | 0.990 | 0.990 | 0.989 | 0.880 | 1.23 |
| DeDrift-Hybrid | 0.990 | 0.990 | 0.990 | 0.990 | 0.888 | 1.22 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.944 | 0.950 | 0.953 | 0.959 | 0.662 | 4.27 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.976 | 0.965 | 0.968 | 0.971 | 0.727 | 3.00 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.977 | 0.974 | 0.975 | 0.978 | 0.774 | 1.80 |
| from scratch on all texts, e-means 3 epochs | 0.990 | 0.991 | 0.991 | 0.993 | 0.899 | 1.15 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.992 | 0.994 | 0.901 | 1.16 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 150.1 |
| initial index: assignment | 30.3 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 2.4 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 3.2 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 2.1 |
| index update: DeDrift-Lazy, median over 10 rounds | 2.5 |
| index update: DeDrift-Split, median over 10 rounds | 0.1 |
| index update: DeDrift-Hybrid, median over 10 rounds | 2.6 |
| reassignment of all vectors, 875000 texts | 33.1 |
| reassignment of all vectors, 1175000 texts | 44.3 |
| reassignment of all vectors, 1550000 texts | 59.0 |
| training: from scratch on all texts, e-means 3 epochs, 875000 texts | 100.3 |
| training: from scratch on all texts, e-means 3 epochs, 1175000 texts | 134.0 |
| training: from scratch on all texts, e-means 3 epochs, 1550000 texts | 178.4 |
| training: from scratch on all texts, e-means 10 epochs (reference), 1550000 texts | 594.1 |
