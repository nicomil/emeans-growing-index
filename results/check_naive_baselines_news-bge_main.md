Insieme di dati: news-bge. Un aggiornamento di un indice da 100000 testi, 2048 centroidi.
Recall@10 leggendo l'1% dell'indice, mediana [min; max] su 3 seed.

### 10000 testi nuovi (circa 5 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.792 [0.791; 0.793] | 0.792 [0.791; 0.793] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.421 [0.403; 0.442] | 0.106 [0.106; 0.109] |
| e-means di Faiss sui nuovi, da righe a caso | 0.396 [0.389; 0.400] | 0.073 [0.069; 0.075] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.604 [0.596; 0.605] | 0.456 [0.440; 0.464] |
| e-means di Faiss con massa iniziale e media mobile | 0.665 [0.662; 0.676] | 0.305 [0.305; 0.312] |
| mini-batch k-means dalle dimensioni delle liste | 0.793 [0.791; 0.794] | 0.793 [0.791; 0.794] |

### 50000 testi nuovi (circa 24 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.773 [0.772; 0.778] | 0.773 [0.772; 0.778] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.684 [0.684; 0.684] | 0.307 [0.304; 0.310] |
| e-means di Faiss sui nuovi, da righe a caso | 0.660 [0.660; 0.663] | 0.255 [0.254; 0.258] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.742 [0.740; 0.746] | 0.674 [0.670; 0.675] |
| e-means di Faiss con massa iniziale e media mobile | 0.752 [0.744; 0.755] | 0.447 [0.442; 0.452] |
| mini-batch k-means dalle dimensioni delle liste | 0.791 [0.791; 0.796] | 0.789 [0.788; 0.794] |
