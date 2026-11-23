faiss 1.16.0: d=64, k=2048, 100000 old rows, 10000 new rows from the same distribution
IndexIVFFlat over all 110000 rows; recall@10 at a search cost >= that of the first row

old centroids, not updated                           recall 0.842 at   880 dist/query   MSE  58.38   imbalance  1.10
from scratch on old + new: e-means, 3 epochs         recall 0.847 at   932 dist/query   MSE  58.40   imbalance  1.10
k-means on new, init = old centroids, 1 iteration    recall 0.826 at   914 dist/query   MSE  64.39   imbalance  1.70
e-means on new, init = old centroids, 1 epoch        recall 0.809 at   938 dist/query   MSE  65.42   imbalance  2.96
  same, unused_threshold=0 (no revival)              recall 0.818 at   992 dist/query   MSE  64.94   imbalance  8.53
e-means on new, init = random rows of new, 1 epoch   recall 0.782 at   941 dist/query   MSE  66.38   imbalance  3.93
e-means on new, init = Gaussian noise, 1 epoch       recall 0.785 at   931 dist/query   MSE  66.21   imbalance  2.81
e-means on new, init = old, usage set, EMA read-out  recall 0.838 at   932 dist/query   MSE  60.99   imbalance  1.18
