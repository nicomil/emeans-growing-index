Dataset: arxiv-full, 1,550,000 texts after 10 rounds, 16,384 centroids, Faiss 1.16.0.
Recall@10 at round 10: mean over seeds 0, 1, 2 and maximum spread between seeds (max − min).

| Strategy | 1% read | spread | 0.1% read | spread |
|---|---|---|---|---|
| never update | 0.989 | 0.000 | 0.867 | 0.002 |
| Faiss e-means on the new texts, from the old centroids (naive use) | 0.085 | 0.005 | 0.056 | 0.002 |
| Faiss k-means on the new texts, one iteration from the old centroids | 0.248 | 0.002 | 0.171 | 0.000 |
| Faiss e-means with initial mass and moving average | 0.991 | 0.001 | 0.880 | 0.002 |
| DeDrift-Lazy | 0.991 | 0.001 | 0.878 | 0.002 |
| DeDrift-Split | 0.989 | 0.001 | 0.879 | 0.007 |
| DeDrift-Hybrid | 0.991 | 0.000 | 0.886 | 0.002 |
| Faiss e-means on the new texts, from the old centroids (naive use) + lists rebuilt | 0.944 | 0.001 | 0.608 | 0.002 |
| Faiss k-means on the new texts, one iteration from the old centroids + lists rebuilt | 0.969 | 0.001 | 0.724 | 0.004 |
| Faiss e-means with initial mass and moving average + lists rebuilt | 0.992 | 0.001 | 0.885 | 0.003 |
| from scratch on all texts, e-means 3 epochs | 0.992 | 0.001 | 0.898 | 0.001 |
| from scratch on all texts, e-means 10 epochs (reference) | 0.992 | 0.001 | 0.903 | 0.001 |
