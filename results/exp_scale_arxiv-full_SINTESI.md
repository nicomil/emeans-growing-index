Insieme di dati: arxiv-full, 1.550.000 testi dopo 10 giri, 16.384 centroidi, Faiss 1.16.0.
Recall@10 al giro 10: media sui seed 0, 1, 2 e scarto massimo fra seed (max − min).

| Strategia | 1% letto | scarto | 0,1% letto | scarto |
|---|---|---|---|---|
| mai aggiornare | 0.989 | 0.000 | 0.867 | 0.002 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) | 0.085 | 0.005 | 0.056 | 0.002 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi | 0.248 | 0.002 | 0.171 | 0.000 |
| e-means di Faiss con massa iniziale e media mobile | 0.991 | 0.001 | 0.880 | 0.002 |
| DeDrift-Lazy | 0.991 | 0.001 | 0.878 | 0.002 |
| DeDrift-Split | 0.989 | 0.001 | 0.879 | 0.007 |
| DeDrift-Hybrid | 0.991 | 0.000 | 0.886 | 0.002 |
| e-means di Faiss sui nuovi, dai centroidi vecchi (uso ingenuo) + liste ricostruite | 0.944 | 0.001 | 0.608 | 0.002 |
| k-means di Faiss sui nuovi, una iterazione dai centroidi vecchi + liste ricostruite | 0.969 | 0.001 | 0.724 | 0.004 |
| e-means di Faiss con massa iniziale e media mobile + liste ricostruite | 0.992 | 0.001 | 0.885 | 0.003 |
| da zero su tutti i testi, e-means 3 epoche | 0.992 | 0.001 | 0.898 | 0.001 |
| da zero su tutti i testi, e-means 10 epoche (riferimento) | 0.992 | 0.001 | 0.903 | 0.001 |
