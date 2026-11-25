Dataset: stackoverflow, seed 1. 800000 initial texts, 10 rounds of 75000, 16384 centroids, 384 dimensions.
Faiss 1.16.0. Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.967 | 0.965 | 0.960 | 0.953 | 0.791 | 1.79 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.375 | 0.100 | 0.081 | 0.108 | 0.054 | 1.16 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.833 | 0.380 | 0.220 | 0.273 | 0.144 | 1.12 |
| Faiss e-means with initial mass and moving average | 0.968 | 0.967 | 0.965 | 0.961 | 0.805 | 1.71 |
| DeDrift-Lazy | 0.967 | 0.967 | 0.965 | 0.961 | 0.803 | 1.73 |
| DeDrift-Split | 0.967 | 0.965 | 0.962 | 0.957 | 0.803 | 1.26 |
| DeDrift-Hybrid | 0.967 | 0.966 | 0.964 | 0.962 | 0.811 | 1.25 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.842 | 0.864 | 0.858 | 0.869 | 0.515 | 7.62 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.940 | 0.920 | 0.912 | 0.919 | 0.625 | 3.36 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.968 | 0.967 | 0.966 | 0.963 | 0.809 | 1.59 |
| from scratch on all texts, e-means 3 epochs | 0.971 | 0.970 | 0.970 | 0.970 | 0.831 | 1.15 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.972 | 0.971 | 0.842 | 1.13 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 153.6 |
| initial index: assignment | 28.4 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 2.9 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 3.0 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 2.9 |
| index update: DeDrift-Lazy, median over 10 rounds | 3.1 |
| index update: DeDrift-Split, median over 10 rounds | 0.1 |
| index update: DeDrift-Hybrid, median over 10 rounds | 2.6 |
| reassignment of all vectors, 875000 texts | 31.1 |
| reassignment of all vectors, 1175000 texts | 41.8 |
| reassignment of all vectors, 1550000 texts | 55.0 |
| training: from scratch on all texts, e-means 3 epochs, 875000 texts | 100.9 |
| training: from scratch on all texts, e-means 3 epochs, 1175000 texts | 135.3 |
| training: from scratch on all texts, e-means 3 epochs, 1550000 texts | 178.5 |
| training: from scratch on all texts, e-means 10 epochs (reference), 1550000 texts | 592.1 |
