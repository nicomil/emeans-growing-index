Insieme di dati: news-bge. Recall@10 leggendo l'1% dell'indice, liste lasciate come sono, mediana [min; max] su 3 seed.

| Aggiornamento sui soli testi nuovi | Dopo 1 giro | Dopo 5 giri | Dopo 10 giri |
|---|---|---|---|
| mai aggiornare | 0.792 [0.791; 0.793] | 0.773 [0.772; 0.778] | 0.745 [0.743; 0.751] |
| Faiss, ingenuo: train(nuovi, init_centroids=vecchi) | 0.114 [0.113; 0.116] | 0.061 [0.061; 0.063] | 0.049 [0.049; 0.051] |
| Faiss, con massa iniziale e lettura della media mobile | 0.792 [0.791; 0.794] | 0.788 [0.786; 0.793] | 0.772 [0.772; 0.773] |
| nostra riscrittura, ingenuo | 0.115 [0.114; 0.116] | 0.062 [0.061; 0.062] | 0.047 [0.047; 0.049] |
| nostra riscrittura, con massa e senza medie finali | 0.792 [0.791; 0.794] | 0.788 [0.786; 0.791] | 0.773 [0.773; 0.775] |
