Dataset: news-bge. One update of an index of 100000 texts, 2048 centroids.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

### 10000 new texts (about 5 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.792 [0.791; 0.793] | 0.792 [0.791; 0.793] |
| Faiss e-means: train(new, init_centroids=old) | 0.332 [0.315; 0.339] | 0.112 [0.107; 0.116] |
| Faiss e-means on the new texts, from random rows | 0.381 [0.301; 0.397] | 0.070 [0.065; 0.071] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.604 [0.596; 0.605] | 0.456 [0.440; 0.464] |
| Faiss e-means with initial mass and moving average | 0.792 [0.791; 0.794] | 0.793 [0.791; 0.794] |
| mini-batch k-means from the list sizes | 0.793 [0.791; 0.794] | 0.793 [0.791; 0.794] |

### 50000 new texts (about 24 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.773 [0.772; 0.778] | 0.773 [0.772; 0.778] |
| Faiss e-means: train(new, init_centroids=old) | 0.657 [0.655; 0.661] | 0.324 [0.322; 0.329] |
| Faiss e-means on the new texts, from random rows | 0.647 [0.639; 0.655] | 0.257 [0.255; 0.258] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.742 [0.740; 0.746] | 0.674 [0.670; 0.675] |
| Faiss e-means with initial mass and moving average | 0.797 [0.796; 0.802] | 0.789 [0.789; 0.794] |
| mini-batch k-means from the list sizes | 0.791 [0.791; 0.796] | 0.789 [0.788; 0.794] |
