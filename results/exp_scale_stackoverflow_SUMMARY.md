Dataset: stackoverflow, 1,550,000 texts after 10 rounds, 16,384 centroids, Faiss 1.16.0.
Recall@10 at round 10: mean over seeds 0, 1, 2 and maximum spread between seeds (max − min).

| Strategy | 1% read | spread | 0.1% read | spread |
|---|---|---|---|---|
| never update | 0.960 | 0.002 | 0.793 | 0.004 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.081 | 0.001 | 0.054 | 0.001 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.223 | 0.006 | 0.148 | 0.006 |
| Faiss e-means with initial mass and moving average | 0.966 | 0.002 | 0.806 | 0.003 |
| DeDrift-Lazy | 0.965 | 0.002 | 0.805 | 0.005 |
| DeDrift-Split | 0.961 | 0.001 | 0.805 | 0.004 |
| DeDrift-Hybrid | 0.965 | 0.001 | 0.813 | 0.004 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.862 | 0.007 | 0.513 | 0.003 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.911 | 0.002 | 0.626 | 0.006 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.967 | 0.001 | 0.811 | 0.004 |
| from scratch on all texts, e-means 3 epochs | 0.971 | 0.000 | 0.832 | 0.002 |
| from scratch on all texts, e-means 10 epochs (reference) | 0.972 | 0.001 | 0.841 | 0.003 |
