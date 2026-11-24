Dataset: arxiv, seed 0. 100000 initial texts, 10 rounds of 10000, 2048 centroids, 384 dimensions.
Faiss 1.16.0. Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.929 | 0.925 | 0.913 | 0.892 | 0.532 | 1.88 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.236 | 0.087 | 0.072 | 0.089 | 0.033 | 1.12 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.809 | 0.379 | 0.230 | 0.277 | 0.095 | 1.13 |
| Faiss e-means with initial mass and moving average | 0.930 | 0.931 | 0.928 | 0.919 | 0.546 | 1.60 |
| DeDrift-Lazy | 0.929 | 0.930 | 0.926 | 0.914 | 0.546 | 1.65 |
| DeDrift-Split | 0.929 | 0.928 | 0.929 | 0.924 | 0.558 | 1.22 |
| DeDrift-Hybrid | 0.929 | 0.931 | 0.931 | 0.927 | 0.570 | 1.21 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.642 | 0.739 | 0.745 | 0.762 | 0.224 | 5.99 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.881 | 0.842 | 0.838 | 0.846 | 0.330 | 2.68 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.930 | 0.932 | 0.933 | 0.925 | 0.555 | 1.49 |
| from scratch on all texts, e-means 3 epochs | 0.933 | 0.935 | 0.944 | 0.942 | 0.599 | 1.17 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.943 | 0.942 | 0.608 | 1.14 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 14.4 |
| initial index: assignment | 1.9 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 0.8 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 0.2 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 0.8 |
| index update: DeDrift-Lazy, median over 10 rounds | 0.6 |
| index update: DeDrift-Split, median over 10 rounds | 0.0 |
| index update: DeDrift-Hybrid, median over 10 rounds | 0.5 |
| reassignment of all vectors, 110000 texts | 2.3 |
| reassignment of all vectors, 150000 texts | 1.9 |
| reassignment of all vectors, 200000 texts | 1.6 |
| training: from scratch on all texts, e-means 3 epochs, 110000 texts | 10.1 |
| training: from scratch on all texts, e-means 3 epochs, 150000 texts | 7.3 |
| training: from scratch on all texts, e-means 3 epochs, 200000 texts | 7.4 |
| training: from scratch on all texts, e-means 10 epochs (reference), 200000 texts | 25.7 |
