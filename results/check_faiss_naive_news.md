Dataset: news. Recall@10 reading 1% of the index, lists kept as they are, median [min; max] over 3 seeds.

| Update on the new texts only | After 1 round | After 5 rounds | After 10 rounds |
|---|---|---|---|
| never update | 0.828 [0.824; 0.830] | 0.806 [0.805; 0.810] | 0.781 [0.779; 0.783] |
| Faiss, naive: train(new, init_centroids=old) | 0.144 [0.143; 0.154] | 0.070 [0.069; 0.074] | 0.052 [0.051; 0.054] |
| Faiss, with initial mass and read-out of the moving average | 0.827 [0.824; 0.830] | 0.819 [0.815; 0.820] | 0.807 [0.804; 0.808] |
| our rewrite, naive | 0.154 [0.150; 0.154] | 0.072 [0.069; 0.076] | 0.053 [0.052; 0.055] |
| our rewrite, with mass and without final means | 0.828 [0.824; 0.829] | 0.819 [0.815; 0.820] | 0.807 [0.804; 0.808] |
