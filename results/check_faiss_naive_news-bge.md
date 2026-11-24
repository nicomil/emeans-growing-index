Dataset: news-bge. Recall@10 reading 1% of the index, lists kept as they are, median [min; max] over 3 seeds.

| Update on the new texts only | After 1 round | After 5 rounds | After 10 rounds |
|---|---|---|---|
| never update | 0.792 [0.791; 0.793] | 0.773 [0.772; 0.778] | 0.745 [0.743; 0.751] |
| Faiss, naive: train(new, init_centroids=old) | 0.114 [0.113; 0.116] | 0.061 [0.061; 0.063] | 0.049 [0.049; 0.051] |
| Faiss, with initial mass and read-out of the moving average | 0.792 [0.791; 0.794] | 0.788 [0.786; 0.793] | 0.772 [0.772; 0.773] |
| our rewrite, naive | 0.115 [0.114; 0.116] | 0.062 [0.061; 0.062] | 0.047 [0.047; 0.049] |
| our rewrite, with mass and without final means | 0.792 [0.791; 0.794] | 0.788 [0.786; 0.791] | 0.773 [0.773; 0.775] |
