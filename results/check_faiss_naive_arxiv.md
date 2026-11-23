Insieme di dati: arxiv. Recall@10 leggendo l'1% dell'indice, liste lasciate come sono, mediana [min; max] su 3 seed.

| Aggiornamento sui soli testi nuovi | Dopo 1 giro | Dopo 5 giri | Dopo 10 giri |
|---|---|---|---|
| mai aggiornare | 0.931 [0.931; 0.932] | 0.929 [0.928; 0.929] | 0.919 [0.915; 0.920] |
| Faiss, ingenuo: train(nuovi, init_centroids=vecchi) | 0.230 [0.218; 0.240] | 0.088 [0.087; 0.091] | 0.069 [0.067; 0.072] |
| Faiss, con massa iniziale e lettura della media mobile | 0.932 [0.930; 0.933] | 0.932 [0.931; 0.932] | 0.930 [0.929; 0.931] |
| nostra riscrittura, ingenuo | 0.229 [0.227; 0.239] | 0.086 [0.085; 0.089] | 0.071 [0.070; 0.072] |
| nostra riscrittura, con massa e senza medie finali | 0.932 [0.930; 0.933] | 0.932 [0.931; 0.933] | 0.931 [0.930; 0.931] |
