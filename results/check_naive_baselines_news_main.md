Dataset: news. One update of an index of 100000 texts, 2048 centroids.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

### 10000 new texts (about 5 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.828 [0.824; 0.830] | 0.828 [0.824; 0.830] |
| Faiss e-means: train(new, init_centroids=old) | 0.512 [0.512; 0.513] | 0.132 [0.130; 0.136] |
| Faiss e-means on the new texts, from random rows | 0.495 [0.462; 0.502] | 0.077 [0.075; 0.079] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.680 [0.679; 0.680] | 0.531 [0.521; 0.535] |
| Faiss e-means with initial mass and moving average | 0.723 [0.710; 0.724] | 0.349 [0.346; 0.359] |
| mini-batch k-means from the list sizes | 0.827 [0.826; 0.829] | 0.827 [0.825; 0.829] |

### 50000 new texts (about 24 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.806 [0.805; 0.810] | 0.806 [0.805; 0.810] |
| Faiss e-means: train(new, init_centroids=old) | 0.739 [0.736; 0.744] | 0.346 [0.342; 0.349] |
| Faiss e-means on the new texts, from random rows | 0.732 [0.729; 0.737] | 0.282 [0.279; 0.283] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.786 [0.782; 0.788] | 0.729 [0.724; 0.732] |
| Faiss e-means with initial mass and moving average | 0.787 [0.787; 0.788] | 0.484 [0.483; 0.501] |
| mini-batch k-means from the list sizes | 0.821 [0.818; 0.821] | 0.820 [0.818; 0.821] |
