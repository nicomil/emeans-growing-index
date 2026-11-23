Insieme di dati: arxiv, seed 0. 100000 testi iniziali, 10 giri da 10000, 2048 centroidi, 384 dimensioni.
Faiss 1.16.0 (ramo principale, compilato dai sorgenti). Recall@10; un solo seed, senza intervalli.

| Strategia | Giro 1: 1% letto | Giro 5: 1% letto | Giro 10: 1% letto | Giro 10: periodo aggiunto | Giro 10: 0,1% letto | Sbilanciamento |
|---|---|---|---|---|---|---|
| mai aggiornare | 0.932 | 0.933 | 0.921 | 0.904 | 0.546 | 1.63 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) | 0.174 | 0.082 | 0.063 | 0.078 | 0.031 | 1.07 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.812 | 0.375 | 0.219 | 0.261 | 0.089 | 1.11 |
| e-means di Faiss con massa iniziale e media mobile | 0.425 | 0.115 | 0.093 | 0.114 | 0.042 | 1.06 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) + liste ricostruite | 0.782 | 0.792 | 0.791 | 0.802 | 0.284 | 3.71 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi + liste ricostruite | 0.883 | 0.841 | 0.847 | 0.852 | 0.335 | 2.59 |
| e-means di Faiss con massa iniziale e media mobile + liste ricostruite | 0.880 | 0.869 | 0.873 | 0.881 | 0.402 | 1.66 |
| da zero su tutti i testi, e-means 3 epoche | 0.937 | 0.936 | 0.942 | 0.944 | 0.606 | 1.13 |
| da zero su tutti i testi, e-means 10 epoche (riferimento) | — | — | 0.945 | 0.945 | 0.609 | 1.13 |

Tempi in secondi (misurati dentro l'esperimento: indicativi se la macchina faceva altro).

| Operazione | Tempo |
|---|---|
| indice iniziale: addestramento, 5 epoche | 5.6 |
| indice iniziale: assegnazione | 1.2 |
| aggiornamento sui nuovi: mai aggiornare, mediana su 10 giri | 0.0 |
| aggiornamento sui nuovi: e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo), mediana su 10 giri | 0.9 |
| aggiornamento sui nuovi: k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi, mediana su 10 giri | 0.2 |
| aggiornamento sui nuovi: e-means di Faiss con massa iniziale e media mobile, mediana su 10 giri | 0.8 |
| riassegnazione di tutti i vettori, 110000 testi | 1.7 |
| riassegnazione di tutti i vettori, 150000 testi | 2.0 |
| riassegnazione di tutti i vettori, 200000 testi | 3.7 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 110000 testi | 3.8 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 150000 testi | 4.3 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 200000 testi | 8.2 |
| addestramento: da zero su tutti i testi, e-means 10 epoche (riferimento), 200000 testi | 29.8 |
