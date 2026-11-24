Dataset: arxiv-full, seed 2. 800000 initial texts, 10 rounds of 75000, 16384 centroids, 384 dimensions.
Faiss 1.16.0. Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.989 | 0.990 | 0.989 | 0.988 | 0.868 | 1.96 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.437 | 0.112 | 0.085 | 0.114 | 0.056 | 1.17 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.883 | 0.419 | 0.247 | 0.317 | 0.171 | 1.14 |
| Faiss e-means with initial mass and moving average | 0.990 | 0.991 | 0.991 | 0.990 | 0.881 | 1.78 |
| DeDrift-Lazy | 0.990 | 0.991 | 0.991 | 0.991 | 0.879 | 1.83 |
| DeDrift-Split | 0.989 | 0.990 | 0.990 | 0.989 | 0.879 | 1.26 |
| DeDrift-Hybrid | 0.990 | 0.991 | 0.991 | 0.991 | 0.886 | 1.25 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.909 | 0.937 | 0.944 | 0.952 | 0.609 | 6.99 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.973 | 0.966 | 0.969 | 0.973 | 0.722 | 2.96 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.990 | 0.991 | 0.992 | 0.991 | 0.887 | 1.67 |
| from scratch on all texts, e-means 3 epochs | 0.990 | 0.992 | 0.991 | 0.992 | 0.898 | 1.18 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.992 | 0.992 | 0.902 | 1.16 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 153.3 |
| initial index: assignment | 28.5 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 2.9 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 3.0 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 2.9 |
| index update: DeDrift-Lazy, median over 10 rounds | 2.9 |
| index update: DeDrift-Split, median over 10 rounds | 0.1 |
| index update: DeDrift-Hybrid, median over 10 rounds | 2.6 |
| reassignment of all vectors, 875000 texts | 31.2 |
| reassignment of all vectors, 1175000 texts | 41.8 |
| reassignment of all vectors, 1550000 texts | 55.4 |
| training: from scratch on all texts, e-means 3 epochs, 875000 texts | 100.7 |
| training: from scratch on all texts, e-means 3 epochs, 1175000 texts | 135.2 |
| training: from scratch on all texts, e-means 3 epochs, 1550000 texts | 185.6 |
| training: from scratch on all texts, e-means 10 epochs (reference), 1550000 texts | 601.0 |
