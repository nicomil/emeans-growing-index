Insieme di dati: msmarco, seed 0. 800000 testi iniziali, 10 giri da 75000, 16384 centroidi, 384 dimensioni.
Faiss 1.16.0. Recall@10; un solo seed, senza intervalli.

| Strategia | Giro 1: 1% letto | Giro 5: 1% letto | Giro 10: 1% letto | Giro 10: periodo aggiunto | Giro 10: 0,1% letto | Sbilanciamento |
|---|---|---|---|---|---|---|
| mai aggiornare | 0.924 | 0.925 | 0.928 | nan | 0.807 | 1.34 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) | 0.345 | 0.104 | 0.080 | nan | 0.055 | 1.22 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.844 | 0.472 | 0.280 | nan | 0.214 | 1.19 |
| e-means di Faiss con massa iniziale e media mobile | 0.924 | 0.926 | 0.929 | nan | 0.807 | 1.32 |
| DeDrift-Lazy | 0.924 | 0.926 | 0.929 | nan | 0.808 | 1.33 |
| DeDrift-Split | 0.924 | 0.925 | 0.928 | nan | 0.807 | 1.24 |
| DeDrift-Hybrid | 0.924 | 0.926 | 0.929 | nan | 0.809 | 1.23 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) + liste ricostruite | 0.776 | 0.823 | 0.830 | nan | 0.568 | 5.76 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi + liste ricostruite | 0.894 | 0.871 | 0.871 | nan | 0.673 | 2.20 |
| e-means di Faiss con massa iniziale e media mobile + liste ricostruite | 0.924 | 0.926 | 0.930 | nan | 0.809 | 1.30 |
| da zero su tutti i testi, e-means 3 epoche | 0.927 | 0.929 | 0.932 | nan | 0.814 | 1.27 |
| da zero su tutti i testi, e-means 10 epoche (riferimento) | — | — | 0.934 | nan | 0.823 | 1.26 |

Tempi in secondi (misurati dentro l'esperimento: indicativi se la macchina faceva altro).

| Operazione | Tempo |
|---|---|
| indice iniziale: addestramento, 5 epoche | 155.3 |
| indice iniziale: assegnazione | 28.4 |
| aggiornamento sui nuovi: mai aggiornare, mediana su 10 giri | 0.0 |
| aggiornamento sui nuovi: e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo), mediana su 10 giri | 2.9 |
| aggiornamento sui nuovi: k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi, mediana su 10 giri | 2.9 |
| aggiornamento sui nuovi: e-means di Faiss con massa iniziale e media mobile, mediana su 10 giri | 2.9 |
| aggiornamento dell'indice: DeDrift-Lazy, mediana su 10 giri | 2.5 |
| aggiornamento dell'indice: DeDrift-Split, mediana su 10 giri | 0.1 |
| aggiornamento dell'indice: DeDrift-Hybrid, mediana su 10 giri | 2.5 |
| riassegnazione di tutti i vettori, 875000 testi | 31.1 |
| riassegnazione di tutti i vettori, 1175000 testi | 41.7 |
| riassegnazione di tutti i vettori, 1550000 testi | 55.0 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 875000 testi | 100.4 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 1175000 testi | 134.8 |
| addestramento: da zero su tutti i testi, e-means 3 epoche, 1550000 testi | 177.8 |
| addestramento: da zero su tutti i testi, e-means 10 epoche (riferimento), 1550000 testi | 591.2 |
