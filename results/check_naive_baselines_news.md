Insieme di dati: news. Un aggiornamento di un indice da 100000 testi, 2048 centroidi.
Recall@10 leggendo l'1% dell'indice, mediana [min; max] su 3 seed.

### 10000 testi nuovi (circa 5 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.828 [0.824; 0.830] | 0.828 [0.824; 0.830] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.417 [0.414; 0.418] | 0.149 [0.144; 0.151] |
| e-means di Faiss sui nuovi, da righe a caso | 0.472 [0.407; 0.494] | 0.076 [0.074; 0.078] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.680 [0.679; 0.680] | 0.531 [0.521; 0.535] |
| e-means di Faiss con massa iniziale e media mobile | 0.827 [0.825; 0.830] | 0.827 [0.825; 0.830] |
| mini-batch k-means dalle dimensioni delle liste | 0.827 [0.826; 0.829] | 0.827 [0.825; 0.829] |

### 50000 testi nuovi (circa 24 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.806 [0.805; 0.810] | 0.806 [0.805; 0.810] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.723 [0.722; 0.726] | 0.381 [0.374; 0.387] |
| e-means di Faiss sui nuovi, da righe a caso | 0.706 [0.700; 0.708] | 0.279 [0.278; 0.280] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.786 [0.782; 0.788] | 0.729 [0.724; 0.732] |
| e-means di Faiss con massa iniziale e media mobile | 0.824 [0.823; 0.825] | 0.821 [0.819; 0.821] |
| mini-batch k-means dalle dimensioni delle liste | 0.821 [0.818; 0.821] | 0.820 [0.818; 0.821] |
