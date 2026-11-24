Dataset: news. One update of an index of 100000 texts, 2048 centroids.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

### 10000 new texts (about 5 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.828 [0.824; 0.830] | 0.828 [0.824; 0.830] |
| Faiss e-means: train(new, init_centroids=old) | 0.417 [0.414; 0.418] | 0.149 [0.144; 0.151] |
| Faiss e-means on the new texts, from random rows | 0.472 [0.407; 0.494] | 0.076 [0.074; 0.078] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.680 [0.679; 0.680] | 0.531 [0.521; 0.535] |
| Faiss e-means with initial mass and moving average | 0.827 [0.825; 0.830] | 0.827 [0.825; 0.830] |
| mini-batch k-means from the list sizes | 0.827 [0.826; 0.829] | 0.827 [0.825; 0.829] |

### 50000 new texts (about 24 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.806 [0.805; 0.810] | 0.806 [0.805; 0.810] |
| Faiss e-means: train(new, init_centroids=old) | 0.723 [0.722; 0.726] | 0.381 [0.374; 0.387] |
| Faiss e-means on the new texts, from random rows | 0.706 [0.700; 0.708] | 0.279 [0.278; 0.280] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.786 [0.782; 0.788] | 0.729 [0.724; 0.732] |
| Faiss e-means with initial mass and moving average | 0.824 [0.823; 0.825] | 0.821 [0.819; 0.821] |
| mini-batch k-means from the list sizes | 0.821 [0.818; 0.821] | 0.820 [0.818; 0.821] |
