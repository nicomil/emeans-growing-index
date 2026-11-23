Insieme di dati: arxiv, seed 0. 100000 testi iniziali, 10 giri da 10000, 2048 centroidi, 384 dimensioni.
Faiss 1.16.0. Recall@10; un solo seed, senza intervalli.

| Strategia | Giro 1: 1% letto | Giro 5: 1% letto | Giro 10: 1% letto | Giro 10: periodo aggiunto | Giro 10: 0,1% letto | Sbilanciamento |
|---|---|---|---|---|---|---|
| mai aggiornare | 0.929 | 0.925 | 0.913 | 0.892 | 0.532 | 1.88 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) | 0.236 | 0.087 | 0.072 | 0.089 | 0.033 | 1.12 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.809 | 0.379 | 0.230 | 0.277 | 0.095 | 1.13 |
| e-means di Faiss con massa iniziale e media mobile | 0.930 | 0.931 | 0.928 | 0.919 | 0.546 | 1.60 |
| DeDrift-Lazy | 0.929 | 0.930 | 0.926 | 0.914 | 0.546 | 1.65 |
| DeDrift-Split | 0.929 | 0.928 | 0.929 | 0.924 | 0.558 | 1.22 |
| DeDrift-Hybrid | 0.929 | 0.931 | 0.931 | 0.927 | 0.570 | 1.21 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) + liste ricostruite | 0.642 | 0.739 | 0.745 | 0.762 | 0.224 | 5.99 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi + liste ricostruite | 0.881 | 0.842 | 0.838 | 0.846 | 0.330 | 2.68 |
| e-means di Faiss con massa iniziale e media mobile + liste ricostruite | 0.930 | 0.932 | 0.933 | 0.925 | 0.555 | 1.49 |
| da zero su tutti i testi, e-means 3 epoche | 0.933 | 0.935 | 0.944 | 0.942 | 0.599 | 1.17 |
| da zero su tutti i testi, e-means 10 epoche (riferimento) | — | — | 0.943 | 0.942 | 0.608 | 1.14 |

Tempi in secondi (misurati dentro l'esperimento: indicativi se la macchina faceva altro).

| Operazione | Tempo |
|---|---|
| indice iniziale: addestramento, 5 epoche | 14.4 |
| indice iniziale: assegnazione | 1.9 |
| aggiornamento sui nuovi: mai aggiornare, mediana su 10 giri | 0.0 |
| aggiornamento sui nuovi: e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo), mediana su 10 giri | 0.8 |
| aggiornamento sui nuovi: k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi, mediana su 10 giri | 0.2 |
| aggiornamento sui nuovi: e-means di Faiss con massa iniziale e media mobile, mediana su 10 giri | 0.8 |
| aggiornamento dell'indice: DeDrift-Lazy, mediana su 10 giri | 0.6 |
| aggiornamento dell'indice: DeDrift-Split, mediana su 10 giri | 0.0 |
| aggiornamento dell'indice: DeDrift-Hybrid, mediana su 10 giri | 0.5 |
| riassegnazione di tutti i vettori, 110000 testi | 2.3 |
| riassegnazione di tutti i vettori, 150000 testi | 1.9 |
| riassegnazione di tutti i vettori, 200000 testi | 1.6 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 110000 testi | 10.1 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 150000 testi | 7.3 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 200000 testi | 7.4 |
| addestramento: da zero su tutti i testi, e-means 10 epoche (riferimento), 200000 testi | 25.7 |
