Dataset: msmarco. 1550000 texts, 16384 centroids, 384 dimensions. Faiss 1.16.0, 8 cores.
Mean over 2 repetitions; maximum load of the machine before a measurement: 2.0.

| Method | Passes over the data | Training (s) | Reassignment (s) | Recall@10, 1% read | Recall@10, 0.1% read |
|---|---|---|---|---|---|
| e-means | 1 | 59.5 | 55.0 | 0.924 | 0.793 |
| e-means | 3 | 177.9 | 55.0 | 0.931 | 0.814 |
| e-means | 5 | 295.8 | 55.0 | 0.933 | 0.818 |
| e-means | 10 | 590.3 | 55.0 | 0.936 | 0.820 |
| k-means | 5 | 276.5 | 55.0 | 0.937 | 0.813 |
| k-means | 10 | 552.6 | 55.0 | 0.937 | 0.820 |
| k-means | 25 | 1381.4 | 55.0 | 0.939 | 0.824 |
