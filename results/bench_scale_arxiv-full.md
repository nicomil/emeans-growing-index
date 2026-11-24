Insieme di dati: arxiv-full. 1550000 testi, 16384 centroidi, 384 dimensioni. Faiss 1.16.0, 8 core.
Media su 2 ripetizioni; carico massimo della macchina prima di una misura: 2.0.

| Metodo | Passate sui dati | Addestramento (s) | Riassegnazione (s) | Recall@10, 1% letto | Recall@10, 0,1% letto |
|---|---|---|---|---|---|
| e-means | 1 | 59.8 | 55.0 | 0.990 | 0.880 |
| e-means | 3 | 177.9 | 55.0 | 0.993 | 0.900 |
| e-means | 5 | 295.7 | 55.6 | 0.992 | 0.903 |
| e-means | 10 | 590.6 | 55.0 | 0.992 | 0.902 |
| k-means | 5 | 276.6 | 55.0 | 0.991 | 0.893 |
| k-means | 10 | 553.0 | 55.0 | 0.992 | 0.898 |
| k-means | 25 | 1382.2 | 55.0 | 0.992 | 0.902 |
