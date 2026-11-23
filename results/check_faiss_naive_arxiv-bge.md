Insieme di dati: arxiv-bge. Recall@10 leggendo l'1% dell'indice, liste lasciate come sono, mediana [min; max] su 3 seed.

| Aggiornamento sui soli testi nuovi | Dopo 1 giro | Dopo 5 giri | Dopo 10 giri |
|---|---|---|---|
| mai aggiornare | 0.937 [0.936; 0.938] | 0.934 [0.933; 0.934] | 0.928 [0.927; 0.929] |
| Faiss, ingenuo: train(nuovi, init_centroids=vecchi) | 0.223 [0.218; 0.234] | 0.083 [0.080; 0.084] | 0.064 [0.064; 0.065] |
| Faiss, con massa iniziale e lettura della media mobile | 0.937 [0.936; 0.938] | 0.937 [0.937; 0.938] | 0.937 [0.935; 0.939] |
| nostra riscrittura, ingenuo | 0.234 [0.233; 0.236] | 0.081 [0.081; 0.086] | 0.068 [0.065; 0.069] |
| nostra riscrittura, con massa e senza medie finali | 0.937 [0.937; 0.937] | 0.937 [0.936; 0.937] | 0.937 [0.936; 0.939] |
