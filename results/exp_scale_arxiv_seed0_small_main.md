Dataset: arxiv, seed 0. 100000 initial texts, 10 rounds of 10000, 2048 centroids, 384 dimensions.
Faiss 1.16.0 (main branch, built from source). Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.932 | 0.933 | 0.921 | 0.904 | 0.546 | 1.63 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.174 | 0.082 | 0.063 | 0.078 | 0.031 | 1.07 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.812 | 0.375 | 0.219 | 0.261 | 0.089 | 1.11 |
| Faiss e-means with initial mass and moving average | 0.425 | 0.115 | 0.093 | 0.114 | 0.042 | 1.06 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.782 | 0.792 | 0.791 | 0.802 | 0.284 | 3.71 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.883 | 0.841 | 0.847 | 0.852 | 0.335 | 2.59 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.880 | 0.869 | 0.873 | 0.881 | 0.402 | 1.66 |
| from scratch on all texts, e-means 3 epochs | 0.937 | 0.936 | 0.942 | 0.944 | 0.606 | 1.13 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.945 | 0.945 | 0.609 | 1.13 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 5.6 |
| initial index: assignment | 1.2 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 0.9 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 0.2 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 0.8 |
| reassignment of all vectors, 110000 texts | 1.7 |
| reassignment of all vectors, 150000 texts | 2.0 |
| reassignment of all vectors, 200000 texts | 3.7 |
| training: from scratch on all texts, e-means 3 epochs, 110000 texts | 3.8 |
| training: from scratch on all texts, e-means 3 epochs, 150000 texts | 4.3 |
| training: from scratch on all texts, e-means 3 epochs, 200000 texts | 8.2 |
| training: from scratch on all texts, e-means 10 epochs (reference), 200000 texts | 29.8 |
