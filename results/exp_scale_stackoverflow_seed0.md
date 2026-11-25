Dataset: stackoverflow, seed 0. 800000 initial texts, 10 rounds of 75000, 16384 centroids, 384 dimensions.
Faiss 1.16.0. Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.969 | 0.966 | 0.959 | 0.952 | 0.796 | 1.78 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.369 | 0.102 | 0.082 | 0.111 | 0.054 | 1.16 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.839 | 0.385 | 0.226 | 0.271 | 0.151 | 1.12 |
| Faiss e-means with initial mass and moving average | 0.970 | 0.968 | 0.966 | 0.961 | 0.808 | 1.70 |
| DeDrift-Lazy | 0.970 | 0.968 | 0.965 | 0.960 | 0.808 | 1.73 |
| DeDrift-Split | 0.969 | 0.966 | 0.961 | 0.955 | 0.807 | 1.26 |
| DeDrift-Hybrid | 0.970 | 0.967 | 0.965 | 0.961 | 0.815 | 1.24 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.840 | 0.866 | 0.865 | 0.876 | 0.513 | 7.61 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.940 | 0.919 | 0.912 | 0.918 | 0.630 | 3.35 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.970 | 0.968 | 0.966 | 0.962 | 0.813 | 1.59 |
| from scratch on all texts, e-means 3 epochs | 0.967 | 0.969 | 0.971 | 0.970 | 0.834 | 1.15 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.972 | 0.972 | 0.839 | 1.13 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 160.4 |
| initial index: assignment | 28.5 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 2.9 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 3.0 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 2.9 |
| index update: DeDrift-Lazy, median over 10 rounds | 3.1 |
| index update: DeDrift-Split, median over 10 rounds | 0.1 |
| index update: DeDrift-Hybrid, median over 10 rounds | 2.6 |
| reassignment of all vectors, 875000 texts | 31.1 |
| reassignment of all vectors, 1175000 texts | 41.7 |
| reassignment of all vectors, 1550000 texts | 55.2 |
| training: from scratch on all texts, e-means 3 epochs, 875000 texts | 100.9 |
| training: from scratch on all texts, e-means 3 epochs, 1175000 texts | 135.3 |
| training: from scratch on all texts, e-means 3 epochs, 1550000 texts | 179.4 |
| training: from scratch on all texts, e-means 10 epochs (reference), 1550000 texts | 596.3 |
