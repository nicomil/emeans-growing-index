Insieme di dati: news. Un aggiornamento di un indice da 100000 testi, 2048 centroidi.
Recall@10 leggendo l'1% dell'indice, mediana [min; max] su 3 seed.

### 10000 testi nuovi (circa 5 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.828 [0.824; 0.830] | 0.828 [0.824; 0.830] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.512 [0.512; 0.513] | 0.132 [0.130; 0.136] |
| e-means di Faiss sui nuovi, da righe a caso | 0.495 [0.462; 0.502] | 0.077 [0.075; 0.079] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.680 [0.679; 0.680] | 0.531 [0.521; 0.535] |
| e-means di Faiss con massa iniziale e media mobile | 0.723 [0.710; 0.724] | 0.349 [0.346; 0.359] |
| mini-batch k-means dalle dimensioni delle liste | 0.827 [0.826; 0.829] | 0.827 [0.825; 0.829] |

### 50000 testi nuovi (circa 24 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.806 [0.805; 0.810] | 0.806 [0.805; 0.810] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.739 [0.736; 0.744] | 0.346 [0.342; 0.349] |
| e-means di Faiss sui nuovi, da righe a caso | 0.732 [0.729; 0.737] | 0.282 [0.279; 0.283] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.786 [0.782; 0.788] | 0.729 [0.724; 0.732] |
| e-means di Faiss con massa iniziale e media mobile | 0.787 [0.787; 0.788] | 0.484 [0.483; 0.501] |
| mini-batch k-means dalle dimensioni delle liste | 0.821 [0.818; 0.821] | 0.820 [0.818; 0.821] |
