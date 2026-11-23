Insieme di dati: news. Recall@10 leggendo l'1% dell'indice, liste lasciate come sono, mediana [min; max] su 3 seed.

| Aggiornamento sui soli testi nuovi | Dopo 1 giro | Dopo 5 giri | Dopo 10 giri |
|---|---|---|---|
| mai aggiornare | 0.828 [0.824; 0.830] | 0.806 [0.805; 0.810] | 0.781 [0.779; 0.783] |
| Faiss, ingenuo: train(nuovi, init_centroids=vecchi) | 0.144 [0.143; 0.154] | 0.070 [0.069; 0.074] | 0.052 [0.051; 0.054] |
| Faiss, con massa iniziale e lettura della media mobile | 0.827 [0.824; 0.830] | 0.819 [0.815; 0.820] | 0.807 [0.804; 0.808] |
| nostra riscrittura, ingenuo | 0.154 [0.150; 0.154] | 0.072 [0.069; 0.076] | 0.053 [0.052; 0.055] |
| nostra riscrittura, con massa e senza medie finali | 0.828 [0.824; 0.829] | 0.819 [0.815; 0.820] | 0.807 [0.804; 0.808] |
