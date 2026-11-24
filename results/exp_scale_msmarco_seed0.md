Dataset: msmarco, seed 0. 800000 initial texts, 10 rounds of 75000, 16384 centroids, 384 dimensions.
Faiss 1.16.0. Recall@10; a single seed, no intervals.

| Strategy | Round 1: 1% read | Round 5: 1% read | Round 10: 1% read | Round 10: added period | Round 10: 0.1% read | Imbalance |
|---|---|---|---|---|---|---|
| never update | 0.924 | 0.925 | 0.928 | nan | 0.807 | 1.34 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.345 | 0.104 | 0.080 | nan | 0.055 | 1.22 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.844 | 0.472 | 0.280 | nan | 0.214 | 1.19 |
| Faiss e-means with initial mass and moving average | 0.924 | 0.926 | 0.929 | nan | 0.807 | 1.32 |
| DeDrift-Lazy | 0.924 | 0.926 | 0.929 | nan | 0.808 | 1.33 |
| DeDrift-Split | 0.924 | 0.925 | 0.928 | nan | 0.807 | 1.24 |
| DeDrift-Hybrid | 0.924 | 0.926 | 0.929 | nan | 0.809 | 1.23 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.776 | 0.823 | 0.830 | nan | 0.568 | 5.76 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.894 | 0.871 | 0.871 | nan | 0.673 | 2.20 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.924 | 0.926 | 0.930 | nan | 0.809 | 1.30 |
| from scratch on all texts, e-means 3 epochs | 0.927 | 0.929 | 0.932 | nan | 0.814 | 1.27 |
| from scratch on all texts, e-means 10 epochs (reference) | — | — | 0.934 | nan | 0.823 | 1.26 |

Times in seconds (measured inside the experiment: indicative if the machine was doing something else).

| Operation | Time |
|---|---|
| initial index: training, 5 epochs | 155.3 |
| initial index: assignment | 28.4 |
| update on the new texts: never update, median over 10 rounds | 0.0 |
| update on the new texts: Faiss e-means on the new texts, from the old centroids (naive use), median over 10 rounds | 2.9 |
| update on the new texts: Faiss k-means on the new texts, one iteration from the old centroids, median over 10 rounds | 2.9 |
| update on the new texts: Faiss e-means with initial mass and moving average, median over 10 rounds | 2.9 |
| index update: DeDrift-Lazy, median over 10 rounds | 2.5 |
| index update: DeDrift-Split, median over 10 rounds | 0.1 |
| index update: DeDrift-Hybrid, median over 10 rounds | 2.5 |
| reassignment of all vectors, 875000 texts | 31.1 |
| reassignment of all vectors, 1175000 texts | 41.7 |
| reassignment of all vectors, 1550000 texts | 55.0 |
| training: from scratch on all texts, e-means 3 epochs, 875000 texts | 100.4 |
| training: from scratch on all texts, e-means 3 epochs, 1175000 texts | 134.8 |
| training: from scratch on all texts, e-means 3 epochs, 1550000 texts | 177.8 |
| training: from scratch on all texts, e-means 10 epochs (reference), 1550000 texts | 591.2 |
