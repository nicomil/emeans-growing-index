Insieme di dati: arxiv. Un aggiornamento di un indice da 100000 testi, 2048 centroidi.
Recall@10 leggendo l'1% dell'indice, mediana [min; max] su 3 seed.

### 10000 testi nuovi (circa 5 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.931 [0.931; 0.932] | 0.931 [0.931; 0.932] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.784 [0.775; 0.788] | 0.193 [0.191; 0.207] |
| e-means di Faiss sui nuovi, da righe a caso | 0.769 [0.767; 0.777] | 0.087 [0.086; 0.090] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.881 [0.879; 0.882] | 0.815 [0.810; 0.821] |
| e-means di Faiss con massa iniziale e media mobile | 0.886 [0.884; 0.887] | 0.447 [0.445; 0.468] |
| mini-batch k-means dalle dimensioni delle liste | 0.932 [0.931; 0.932] | 0.932 [0.931; 0.932] |

### 50000 testi nuovi (circa 24 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.929 [0.928; 0.929] | 0.929 [0.928; 0.929] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.907 [0.904; 0.909] | 0.441 [0.439; 0.446] |
| e-means di Faiss sui nuovi, da righe a caso | 0.900 [0.900; 0.902] | 0.316 [0.313; 0.316] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.929 [0.926; 0.930] | 0.922 [0.919; 0.923] |
| e-means di Faiss con massa iniziale e media mobile | 0.925 [0.924; 0.927] | 0.721 [0.702; 0.724] |
| mini-batch k-means dalle dimensioni delle liste | 0.934 [0.933; 0.934] | 0.933 [0.932; 0.933] |
