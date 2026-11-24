Dataset: arxiv. One update of an index of 100000 texts, 2048 centroids.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

### 10000 new texts (about 5 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.931 [0.931; 0.932] | 0.931 [0.931; 0.932] |
| Faiss e-means: train(new, init_centroids=old) | 0.784 [0.775; 0.788] | 0.193 [0.191; 0.207] |
| Faiss e-means on the new texts, from random rows | 0.769 [0.767; 0.777] | 0.087 [0.086; 0.090] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.881 [0.879; 0.882] | 0.815 [0.810; 0.821] |
| Faiss e-means with initial mass and moving average | 0.886 [0.884; 0.887] | 0.447 [0.445; 0.468] |
| mini-batch k-means from the list sizes | 0.932 [0.931; 0.932] | 0.932 [0.931; 0.932] |

### 50000 new texts (about 24 per centroid)

| Centroids updated on the new texts only | Lists rebuilt | Lists kept as they are |
|---|---|---|
| never update | 0.929 [0.928; 0.929] | 0.929 [0.928; 0.929] |
| Faiss e-means: train(new, init_centroids=old) | 0.907 [0.904; 0.909] | 0.441 [0.439; 0.446] |
| Faiss e-means on the new texts, from random rows | 0.900 [0.900; 0.902] | 0.316 [0.313; 0.316] |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.929 [0.926; 0.930] | 0.922 [0.919; 0.923] |
| Faiss e-means with initial mass and moving average | 0.925 [0.924; 0.927] | 0.721 [0.702; 0.724] |
| mini-batch k-means from the list sizes | 0.934 [0.933; 0.934] | 0.933 [0.932; 0.933] |
