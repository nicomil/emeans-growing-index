Insieme di dati: arxiv-bge. Un aggiornamento di un indice da 100000 testi, 2048 centroidi.
Recall@10 leggendo l'1% dell'indice, mediana [min; max] su 3 seed.

### 10000 testi nuovi (circa 5 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.937 [0.936; 0.938] | 0.937 [0.936; 0.938] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.785 [0.783; 0.790] | 0.204 [0.202; 0.207] |
| e-means di Faiss sui nuovi, da righe a caso | 0.785 [0.769; 0.786] | 0.093 [0.091; 0.094] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.889 [0.885; 0.889] | 0.807 [0.797; 0.808] |
| e-means di Faiss con massa iniziale e media mobile | 0.891 [0.889; 0.894] | 0.458 [0.450; 0.465] |
| mini-batch k-means dalle dimensioni delle liste | 0.937 [0.937; 0.937] | 0.937 [0.936; 0.937] |

### 50000 testi nuovi (circa 24 per centroide)

| Centroidi aggiornati sui soli testi nuovi | Liste ricostruite | Liste lasciate come sono |
|---|---|---|
| mai aggiornare | 0.934 [0.933; 0.934] | 0.934 [0.933; 0.934] |
| e-means di Faiss: train(nuovi, init_centroids=vecchi) | 0.916 [0.913; 0.918] | 0.425 [0.424; 0.436] |
| e-means di Faiss sui nuovi, da righe a caso | 0.910 [0.909; 0.912] | 0.313 [0.312; 0.313] |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.932 [0.931; 0.934] | 0.926 [0.924; 0.927] |
| e-means di Faiss con massa iniziale e media mobile | 0.931 [0.930; 0.932] | 0.711 [0.696; 0.715] |
| mini-batch k-means dalle dimensioni delle liste | 0.938 [0.936; 0.939] | 0.938 [0.936; 0.938] |
