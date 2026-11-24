Dataset: arxiv-full. 1550000 texts, 16384 centroids, 384 dimensions. Faiss 1.16.0, 8 cores.
Mean over 2 repetitions; maximum load of the machine before a measurement: 2.0.

| Method | Passes over the data | Training (s) | Reassignment (s) | Recall@10, 1% read | Recall@10, 0.1% read |
|---|---|---|---|---|---|
| e-means | 1 | 59.8 | 55.0 | 0.990 | 0.880 |
| e-means | 3 | 177.9 | 55.0 | 0.993 | 0.900 |
| e-means | 5 | 295.7 | 55.6 | 0.992 | 0.903 |
| e-means | 10 | 590.6 | 55.0 | 0.992 | 0.902 |
| k-means | 5 | 276.6 | 55.0 | 0.991 | 0.893 |
| k-means | 10 | 553.0 | 55.0 | 0.992 | 0.898 |
| k-means | 25 | 1382.2 | 55.0 | 0.992 | 0.902 |
