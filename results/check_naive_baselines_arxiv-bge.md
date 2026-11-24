Dataset: arxiv-bge. One update of an index of 100000 texts, 2048 centroids.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

### 10000 new texts (about 5 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.937 [0.936; 0.938] | 0.937 [0.936; 0.938] |
| Faiss e-means: train(new, init_centroids=old) | 0.657 [0.656; 0.670] | 0.236 [0.224; 0.239] |
| Faiss e-means on the new texts, from random rows | 0.754 [0.650; 0.765] | 0.090 [0.089; 0.091] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.889 [0.885; 0.889] | 0.807 [0.797; 0.808] |
| Faiss e-means with initial mass and moving average | 0.937 [0.937; 0.938] | 0.937 [0.936; 0.938] |
| mini-batch k-means from the list sizes | 0.937 [0.937; 0.937] | 0.937 [0.936; 0.937] |

### 50000 new texts (about 24 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.934 [0.933; 0.934] | 0.934 [0.933; 0.934] |
| Faiss e-means: train(new, init_centroids=old) | 0.905 [0.901; 0.908] | 0.475 [0.473; 0.489] |
| Faiss e-means on the new texts, from random rows | 0.900 [0.898; 0.900] | 0.312 [0.310; 0.315] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.932 [0.931; 0.934] | 0.926 [0.924; 0.927] |
| Faiss e-means with initial mass and moving average | 0.938 [0.938; 0.939] | 0.936 [0.935; 0.936] |
| mini-batch k-means from the list sizes | 0.938 [0.936; 0.939] | 0.938 [0.936; 0.938] |
