Dataset: arxiv-bge. One update of an index of 100000 texts, 2048 centroids.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

### 10000 new texts (about 5 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.937 [0.936; 0.938] | 0.937 [0.936; 0.938] |
| Faiss e-means: train(new, init_centroids=old) | 0.785 [0.783; 0.790] | 0.204 [0.202; 0.207] |
| Faiss e-means on the new texts, from random rows | 0.785 [0.769; 0.786] | 0.093 [0.091; 0.094] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.889 [0.885; 0.889] | 0.807 [0.797; 0.808] |
| Faiss e-means with initial mass and moving average | 0.891 [0.889; 0.894] | 0.458 [0.450; 0.465] |
| mini-batch k-means from the list sizes | 0.937 [0.937; 0.937] | 0.937 [0.936; 0.937] |

### 50000 new texts (about 24 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.934 [0.933; 0.934] | 0.934 [0.933; 0.934] |
| Faiss e-means: train(new, init_centroids=old) | 0.916 [0.913; 0.918] | 0.425 [0.424; 0.436] |
| Faiss e-means on the new texts, from random rows | 0.910 [0.909; 0.912] | 0.313 [0.312; 0.313] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.932 [0.931; 0.934] | 0.926 [0.924; 0.927] |
| Faiss e-means with initial mass and moving average | 0.931 [0.930; 0.932] | 0.711 [0.696; 0.715] |
| mini-batch k-means from the list sizes | 0.938 [0.936; 0.939] | 0.938 [0.936; 0.938] |
