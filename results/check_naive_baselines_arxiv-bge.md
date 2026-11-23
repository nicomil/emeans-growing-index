Insieme di dati: arxiv-bge. Un aggiornamento di un indice da 100000 testi, 2048 centroidi.
Recall@10 leggendo l'1% dell'indice, mediana [min; max] su 3 seed.

### 10000 testi nuovi (circa 5 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.937 [0.936; 0.938] | 0.937 [0.936; 0.938] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.657 [0.656; 0.670] | 0.236 [0.224; 0.239] |
| e-means di Faiss sui nuovi, da righe a caso | 0.754 [0.650; 0.765] | 0.090 [0.089; 0.091] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.889 [0.885; 0.889] | 0.807 [0.797; 0.808] |
| e-means di Faiss con massa iniziale e media mobile | 0.937 [0.937; 0.938] | 0.937 [0.936; 0.938] |
| mini-batch k-means dalle dimensioni delle liste | 0.937 [0.937; 0.937] | 0.937 [0.936; 0.937] |

### 50000 testi nuovi (circa 24 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.934 [0.933; 0.934] | 0.934 [0.933; 0.934] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.905 [0.901; 0.908] | 0.475 [0.473; 0.489] |
| e-means di Faiss sui nuovi, da righe a caso | 0.900 [0.898; 0.900] | 0.312 [0.310; 0.315] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.932 [0.931; 0.934] | 0.926 [0.924; 0.927] |
| e-means di Faiss con massa iniziale e media mobile | 0.938 [0.938; 0.939] | 0.936 [0.935; 0.936] |
| mini-batch k-means dalle dimensioni delle liste | 0.938 [0.936; 0.939] | 0.938 [0.936; 0.938] |
