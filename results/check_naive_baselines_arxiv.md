Dataset: arxiv. One update of an index of 100000 texts, 2048 centroids.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

### 10000 new texts (about 5 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.931 [0.931; 0.932] | 0.931 [0.931; 0.932] |
| Faiss e-means: train(new, init_centroids=old) | 0.656 [0.656; 0.667] | 0.238 [0.236; 0.245] |
| Faiss e-means on the new texts, from random rows | 0.733 [0.666; 0.739] | 0.087 [0.086; 0.090] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.881 [0.879; 0.882] | 0.815 [0.810; 0.821] |
| Faiss e-means with initial mass and moving average | 0.932 [0.931; 0.934] | 0.932 [0.931; 0.932] |
| mini-batch k-means from the list sizes | 0.932 [0.931; 0.932] | 0.932 [0.931; 0.932] |

### 50000 new texts (about 24 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.929 [0.928; 0.929] | 0.929 [0.928; 0.929] |
| Faiss e-means: train(new, init_centroids=old) | 0.892 [0.892; 0.896] | 0.492 [0.485; 0.494] |
| Faiss e-means on the new texts, from random rows | 0.889 [0.887; 0.890] | 0.312 [0.312; 0.316] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.929 [0.926; 0.930] | 0.922 [0.919; 0.923] |
| Faiss e-means with initial mass and moving average | 0.934 [0.933; 0.935] | 0.930 [0.929; 0.932] |
| mini-batch k-means from the list sizes | 0.934 [0.933; 0.934] | 0.933 [0.932; 0.933] |
