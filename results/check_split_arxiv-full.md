Insieme di dati: arxiv-full, seed 0. 800000 testi iniziali, 10 giri da 75000, 16384 centroidi.
Recall@10 dopo 10 giri; un solo seed, senza intervalli.

| Strategia | 1% letto | 0,1% letto | Sbilanciamento |
|---|---|---|---|
| mai aggiornare | 0.989 | 0.866 | 1.94 |
| DeDrift-Lazy | 0.990 | 0.877 | 1.83 |
| DeDrift-Split, 10 iterazioni da punti a caso (come in exp_scale.py) | 0.989 | 0.875 | 1.26 |
| DeDrift-Hybrid, 10 iterazioni da punti a caso (come in exp_scale.py) | 0.991 | 0.885 | 1.25 |
| DeDrift-Split, 5 iterazioni da punti a caso | 0.989 | 0.875 | 1.26 |
| DeDrift-Hybrid, 5 iterazioni da punti a caso | 0.990 | 0.884 | 1.25 |
| DeDrift-Split, 25 iterazioni da punti a caso | 0.989 | 0.876 | 1.26 |
| DeDrift-Hybrid, 25 iterazioni da punti a caso | 0.990 | 0.883 | 1.25 |
| DeDrift-Split, 10 iterazioni dai centroidi vecchi | 0.989 | 0.867 | 2.04 |
| DeDrift-Hybrid, 10 iterazioni dai centroidi vecchi | 0.990 | 0.878 | 1.81 |
