Insieme di dati: arxiv-full, seed 1. 800000 testi iniziali, 10 giri da 75000, 16384 centroidi, 384 dimensioni.
Faiss 1.16.0. Recall@10; un solo seed, senza intervalli.

| Strategia | Giro 1: 1% letto | Giro 5: 1% letto | Giro 10: 1% letto | Giro 10: periodo aggiunto | Giro 10: 0,1% letto | Sbilanciamento |
|---|---|---|---|---|---|---|
| mai aggiornare | 0.989 | 0.990 | 0.989 | 0.987 | 0.868 | 1.96 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) | 0.445 | 0.109 | 0.087 | 0.118 | 0.057 | 1.17 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.878 | 0.416 | 0.249 | 0.321 | 0.171 | 1.14 |
| e-means di Faiss con massa iniziale e media mobile | 0.989 | 0.991 | 0.991 | 0.990 | 0.880 | 1.78 |
| DeDrift-Lazy | 0.989 | 0.991 | 0.991 | 0.990 | 0.879 | 1.83 |
| DeDrift-Split | 0.989 | 0.990 | 0.989 | 0.989 | 0.882 | 1.26 |
| DeDrift-Hybrid | 0.989 | 0.991 | 0.991 | 0.991 | 0.887 | 1.25 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) + liste ricostruite | 0.910 | 0.936 | 0.945 | 0.952 | 0.607 | 6.96 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi + liste ricostruite | 0.975 | 0.966 | 0.969 | 0.973 | 0.725 | 2.92 |
| e-means di Faiss con massa iniziale e media mobile + liste ricostruite | 0.989 | 0.992 | 0.992 | 0.991 | 0.885 | 1.67 |
| da zero su tutti i testi, e-means 3 epoche | 0.990 | 0.990 | 0.992 | 0.993 | 0.898 | 1.18 |
| da zero su tutti i testi, e-means 10 epoche (riferimento) | — | — | 0.992 | 0.993 | 0.903 | 1.17 |

Tempi in secondi (misurati dentro l'esperimento: indicativi se la macchina faceva altro).

| Operazione | Tempo |
|---|---|
| indice iniziale: addestramento, 5 epoche | 153.1 |
| indice iniziale: assegnazione | 28.5 |
| aggiornamento sui nuovi: mai aggiornare, mediana su 10 giri | 0.0 |
| aggiornamento sui nuovi: e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo), mediana su 10 giri | 2.9 |
| aggiornamento sui nuovi: k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi, mediana su 10 giri | 3.0 |
| aggiornamento sui nuovi: e-means di Faiss con massa iniziale e media mobile, mediana su 10 giri | 2.9 |
| aggiornamento dell'indice: DeDrift-Lazy, mediana su 10 giri | 3.1 |
| aggiornamento dell'indice: DeDrift-Split, mediana su 10 giri | 0.1 |
| aggiornamento dell'indice: DeDrift-Hybrid, mediana su 10 giri | 2.7 |
| riassegnazione di tutti i vettori, 875000 testi | 31.3 |
| riassegnazione di tutti i vettori, 1175000 testi | 41.9 |
| riassegnazione di tutti i vettori, 1550000 testi | 55.1 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 875000 testi | 100.8 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 1175000 testi | 136.0 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 1550000 testi | 179.1 |
| addestramento: da zero su tutti i testi, e-means 10 epoche (riferimento), 1550000 testi | 593.3 |
