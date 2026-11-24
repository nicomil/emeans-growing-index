Dataset: arxiv-full, seed 1. 800000 initial texts, 10 rounds of 75000, 16384 centroids, 384 dimensions.
Faiss 1.16.0. Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.989 | 0.990 | 0.989 | 0.987 | 0.868 | 1.96 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.445 | 0.109 | 0.087 | 0.118 | 0.057 | 1.17 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.878 | 0.416 | 0.249 | 0.321 | 0.171 | 1.14 |
| Faiss e-means with initial mass and moving average | 0.989 | 0.991 | 0.991 | 0.990 | 0.880 | 1.78 |
| DeDrift-Lazy | 0.989 | 0.991 | 0.991 | 0.990 | 0.879 | 1.83 |
| DeDrift-Split | 0.989 | 0.990 | 0.989 | 0.989 | 0.882 | 1.26 |
| DeDrift-Hybrid | 0.989 | 0.991 | 0.991 | 0.991 | 0.887 | 1.25 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.910 | 0.936 | 0.945 | 0.952 | 0.607 | 6.96 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.975 | 0.966 | 0.969 | 0.973 | 0.725 | 2.92 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.989 | 0.992 | 0.992 | 0.991 | 0.885 | 1.67 |
| from scratch on all texts, e-means 3 epochs | 0.990 | 0.990 | 0.992 | 0.993 | 0.898 | 1.18 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.992 | 0.993 | 0.903 | 1.17 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 153.1 |
| initial index: assignment | 28.5 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 2.9 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 3.0 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 2.9 |
| index update: DeDrift-Lazy, median over 10 rounds | 3.1 |
| index update: DeDrift-Split, median over 10 rounds | 0.1 |
| index update: DeDrift-Hybrid, median over 10 rounds | 2.7 |
| reassignment of all vectors, 875000 texts | 31.3 |
| reassignment of all vectors, 1175000 texts | 41.9 |
| reassignment of all vectors, 1550000 texts | 55.1 |
| training: from scratch on all texts, e-means 3 epochs, 875000 texts | 100.8 |
| training: from scratch on all texts, e-means 3 epochs, 1175000 texts | 136.0 |
| training: from scratch on all texts, e-means 3 epochs, 1550000 texts | 179.1 |
| training: from scratch on all texts, e-means 10 epochs (reference), 1550000 texts | 593.3 |
