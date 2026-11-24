Dataset: arxiv. Recall@10 reading 1% of the index, lists kept as they are, median [min; max] over 3 seeds.

| Update on the new texts only | After 1 round | After 5 rounds | After 10 rounds |
|---|---|---|---|
| never update | 0.931 [0.931; 0.932] | 0.929 [0.928; 0.929] | 0.919 [0.915; 0.920] |
| Faiss, naive: train(new, init_centroids=old) | 0.230 [0.218; 0.240] | 0.088 [0.087; 0.091] | 0.069 [0.067; 0.072] |
| Faiss, with initial mass and read-out of the moving average | 0.932 [0.930; 0.933] | 0.932 [0.931; 0.932] | 0.930 [0.929; 0.931] |
| our rewrite, naive | 0.229 [0.227; 0.239] | 0.086 [0.085; 0.089] | 0.071 [0.070; 0.072] |
| our rewrite, with mass and without final means | 0.932 [0.930; 0.933] | 0.932 [0.931; 0.933] | 0.931 [0.930; 0.931] |
