Insieme di dati: arxiv. Un aggiornamento di un indice da 100000 testi, 2048 centroidi.
Recall@10 leggendo l'1% dell'indice, mediana [min; max] su 3 seed.

### 10000 testi nuovi (circa 5 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.931 [0.931; 0.932] | 0.931 [0.931; 0.932] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.656 [0.656; 0.667] | 0.238 [0.236; 0.245] |
| e-means di Faiss sui nuovi, da righe a caso | 0.733 [0.666; 0.739] | 0.087 [0.086; 0.090] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.881 [0.879; 0.882] | 0.815 [0.810; 0.821] |
| e-means di Faiss con massa iniziale e media mobile | 0.932 [0.931; 0.934] | 0.932 [0.931; 0.932] |
| mini-batch k-means dalle dimensioni delle liste | 0.932 [0.931; 0.932] | 0.932 [0.931; 0.932] |

### 50000 testi nuovi (circa 24 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.929 [0.928; 0.929] | 0.929 [0.928; 0.929] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.892 [0.892; 0.896] | 0.492 [0.485; 0.494] |
| e-means di Faiss sui nuovi, da righe a caso | 0.889 [0.887; 0.890] | 0.312 [0.312; 0.316] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.929 [0.926; 0.930] | 0.922 [0.919; 0.923] |
| e-means di Faiss con massa iniziale e media mobile | 0.934 [0.933; 0.935] | 0.930 [0.929; 0.932] |
| mini-batch k-means dalle dimensioni delle liste | 0.934 [0.933; 0.934] | 0.933 [0.932; 0.933] |
