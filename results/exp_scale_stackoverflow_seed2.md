Dataset: stackoverflow, seed 2. 800000 initial texts, 10 rounds of 75000, 16384 centroids, 384 dimensions.
Faiss 1.16.0. Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.969 | 0.965 | 0.961 | 0.953 | 0.792 | 1.79 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.359 | 0.101 | 0.081 | 0.107 | 0.053 | 1.16 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.841 | 0.387 | 0.224 | 0.275 | 0.148 | 1.12 |
| Faiss e-means with initial mass and moving average | 0.969 | 0.967 | 0.966 | 0.962 | 0.806 | 1.71 |
| DeDrift-Lazy | 0.969 | 0.967 | 0.966 | 0.962 | 0.805 | 1.74 |
| DeDrift-Split | 0.969 | 0.965 | 0.962 | 0.956 | 0.805 | 1.25 |
| DeDrift-Hybrid | 0.969 | 0.967 | 0.965 | 0.962 | 0.814 | 1.25 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.845 | 0.867 | 0.864 | 0.878 | 0.512 | 7.46 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.942 | 0.920 | 0.910 | 0.916 | 0.624 | 3.50 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.969 | 0.968 | 0.968 | 0.964 | 0.812 | 1.60 |
| from scratch on all texts, e-means 3 epochs | 0.967 | 0.969 | 0.971 | 0.971 | 0.832 | 1.15 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.972 | 0.972 | 0.841 | 1.13 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 153.5 |
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
| reassignment of all vectors, 1550000 texts | 55.3 |
| training: from scratch on all texts, e-means 3 epochs, 875000 texts | 100.9 |
| training: from scratch on all texts, e-means 3 epochs, 1175000 texts | 135.2 |
| training: from scratch on all texts, e-means 3 epochs, 1550000 texts | 178.6 |
| training: from scratch on all texts, e-means 10 epochs (reference), 1550000 texts | 596.5 |
