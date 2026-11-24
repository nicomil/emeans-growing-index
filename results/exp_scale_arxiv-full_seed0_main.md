Insieme di dati: arxiv-full, seed 0. 800000 testi iniziali, 10 giri da 75000, 16384 centroidi, 384 dimensioni.
Faiss 1.16.0 (ramo principale, compilato dai sorgenti). Recall@10; un solo seed, senza intervalli.

| Strategia | Giro 1: 1% letto | Giro 5: 1% letto | Giro 10: 1% letto | Giro 10: periodo aggiunto | Giro 10: 0,1% letto | Sbilanciamento |
|---|---|---|---|---|---|---|
| mai aggiornare | 0.990 | 0.990 | 0.989 | 0.988 | 0.870 | 1.82 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) | 0.270 | 0.084 | 0.067 | 0.090 | 0.049 | 1.09 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.885 | 0.410 | 0.249 | 0.314 | 0.173 | 1.12 |
| e-means di Faiss con massa iniziale e media mobile | 0.454 | 0.122 | 0.091 | 0.122 | 0.068 | 1.07 |
| DeDrift-Lazy | 0.990 | 0.990 | 0.991 | 0.990 | 0.882 | 1.72 |
| DeDrift-Split | 0.990 | 0.990 | 0.990 | 0.989 | 0.880 | 1.23 |
| DeDrift-Hybrid | 0.990 | 0.990 | 0.990 | 0.990 | 0.888 | 1.22 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) + liste ricostruite | 0.944 | 0.950 | 0.953 | 0.959 | 0.662 | 4.27 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi + liste ricostruite | 0.976 | 0.965 | 0.968 | 0.971 | 0.727 | 3.00 |
| e-means di Faiss con massa iniziale e media mobile + liste ricostruite | 0.977 | 0.974 | 0.975 | 0.978 | 0.774 | 1.80 |
| da zero su tutti i testi, e-means 3 epoche | 0.990 | 0.991 | 0.991 | 0.993 | 0.899 | 1.15 |
| da zero su tutti i testi, e-means 10 epoche (riferimento) | — | — | 0.992 | 0.994 | 0.901 | 1.16 |

Tempi in secondi (misurati dentro l'esperimento: indicativi se la macchina faceva altro).

| Operazione | Tempo |
|---|---|
| indice iniziale: addestramento, 5 epoche | 150.1 |
| indice iniziale: assegnazione | 30.3 |
| aggiornamento sui nuovi: mai aggiornare, mediana su 10 giri | 0.0 |
| aggiornamento sui nuovi: e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo), mediana su 10 giri | 2.4 |
| aggiornamento sui nuovi: k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi, mediana su 10 giri | 3.2 |
| aggiornamento sui nuovi: e-means di Faiss con massa iniziale e media mobile, mediana su 10 giri | 2.1 |
| aggiornamento dell'indice: DeDrift-Lazy, mediana su 10 giri | 2.5 |
| aggiornamento dell'indice: DeDrift-Split, mediana su 10 giri | 0.1 |
| aggiornamento dell'indice: DeDrift-Hybrid, mediana su 10 giri | 2.6 |
| riassegnazione di tutti i vettori, 875000 testi | 33.1 |
| riassegnazione di tutti i vettori, 1175000 testi | 44.3 |
| riassegnazione di tutti i vettori, 1550000 testi | 59.0 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 875000 testi | 100.3 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 1175000 testi | 134.0 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 1550000 testi | 178.4 |
| addestramento: da zero su tutti i testi, e-means 10 epoche (riferimento), 1550000 testi | 594.1 |
