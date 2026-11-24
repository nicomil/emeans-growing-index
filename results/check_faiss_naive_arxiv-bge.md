Dataset: arxiv-bge. Recall@10 reading 1% of the index, lists kept as they are, median [min; max] over 3 seeds.

| Update on the new texts only | After 1 round | After 5 rounds | After 10 rounds |
|---|---|---|---|
| never update | 0.937 [0.936; 0.938] | 0.934 [0.933; 0.934] | 0.928 [0.927; 0.929] |
| Faiss, naive: train(new, init_centroids=old) | 0.223 [0.218; 0.234] | 0.083 [0.080; 0.084] | 0.064 [0.064; 0.065] |
| Faiss, with initial mass and read-out of the moving average | 0.937 [0.936; 0.938] | 0.937 [0.937; 0.938] | 0.937 [0.935; 0.939] |
| our rewrite, naive | 0.234 [0.233; 0.236] | 0.081 [0.081; 0.086] | 0.068 [0.065; 0.069] |
| our rewrite, with mass and without final means | 0.937 [0.937; 0.937] | 0.937 [0.936; 0.937] | 0.937 [0.936; 0.939] |
