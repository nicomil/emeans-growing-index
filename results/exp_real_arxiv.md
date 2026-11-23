Insieme di dati: arxiv, 384 dimensioni.
Indice iniziale: 100000 testi, dal 2007-04-01 al 2016-08-01.
10 giri da 10000 testi, fino al 2021-09-01. 2048 liste, 3 seed dell'algoritmo.
Recall@10 leggendo lo 0,1% e l'1% dell'indice. Mediana su 3 seed. Gli intervalli sono in results/SINTESI.md.


### Dopo 1 giro (indice fino al 2017-04-01; 1534 interrogazioni, di cui 145 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +0.73% | 0.558 | 0.931 | 0.929 |
| e-means di Faiss 1.16.0, impostazioni di serie | +135.05% | 0.084 | 0.230 | 0.292 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +25.84% | 0.169 | 0.652 | 0.676 |
| e-means: massa no, rianimazione sì, medie finali sì | +137.38% | 0.083 | 0.229 | 0.269 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +25.88% | 0.173 | 0.660 | 0.685 |
| e-means: massa no, rianimazione sì, medie finali no | +149.56% | 0.056 | 0.181 | 0.221 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +26.75% | 0.192 | 0.673 | 0.685 |
| e-means: massa no, rianimazione no, medie finali sì | +88.82% | 0.136 | 0.391 | 0.392 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +24.10% | 0.167 | 0.677 | 0.702 |
| e-means: massa no, rianimazione no, medie finali no | +89.20% | 0.134 | 0.392 | 0.399 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +24.94% | 0.167 | 0.666 | 0.690 |
| e-means: massa sì, rianimazione sì, medie finali sì | +25.83% | 0.447 | 0.836 | 0.839 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +15.75% | 0.439 | 0.883 | 0.878 |
| e-means: massa sì, rianimazione sì, medie finali no | +0.54% | 0.560 | 0.932 | 0.929 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +0.53% | 0.561 | 0.933 | 0.928 |
| e-means: massa sì, rianimazione no, medie finali sì | +25.83% | 0.447 | 0.836 | 0.839 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +15.75% | 0.439 | 0.883 | 0.878 |
| e-means: massa sì, rianimazione no, medie finali no | +0.54% | 0.560 | 0.932 | 0.929 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +0.53% | 0.561 | 0.933 | 0.928 |
| mini-batch k-means dalle dimensioni delle liste | +0.51% | 0.560 | 0.932 | 0.930 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +0.50% | 0.561 | 0.932 | 0.930 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +1.38% | 0.555 | 0.931 | 0.922 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +1.24% | 0.556 | 0.931 | 0.923 |
| a caldo, 1 epoca a giro | +4.02% | 0.506 | 0.920 | 0.914 |
| a caldo, 3 epoche a giro | +0.60% | 0.554 | 0.931 | 0.923 |
| a caldo con massa a regime, 3 epoche a giro | +0.24% | 0.562 | 0.933 | 0.926 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.37% | 0.560 | 0.932 | 0.928 |
| da zero, 1 epoca | +4.46% | 0.501 | 0.918 | 0.920 |
| da zero, 3 epoche | +0.87% | 0.551 | 0.931 | 0.929 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.565 | 0.934 | 0.926 |

### Dopo 5 giri (indice fino al 2019-07-01; 2145 interrogazioni, di cui 756 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +2.31% | 0.549 | 0.929 | 0.917 |
| e-means di Faiss 1.16.0, impostazioni di serie | +197.40% | 0.041 | 0.088 | 0.115 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +23.16% | 0.224 | 0.743 | 0.750 |
| e-means: massa no, rianimazione sì, medie finali sì | +197.71% | 0.042 | 0.086 | 0.112 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +23.30% | 0.215 | 0.738 | 0.746 |
| e-means: massa no, rianimazione sì, medie finali no | +186.65% | 0.032 | 0.077 | 0.098 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +24.33% | 0.223 | 0.719 | 0.727 |
| e-means: massa no, rianimazione no, medie finali sì | +109.41% | 0.060 | 0.246 | 0.284 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +29.90% | 0.091 | 0.484 | 0.509 |
| e-means: massa no, rianimazione no, medie finali no | +109.46% | 0.058 | 0.249 | 0.292 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +31.01% | 0.090 | 0.468 | 0.489 |
| e-means: massa sì, rianimazione sì, medie finali sì | +53.27% | 0.287 | 0.619 | 0.652 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +17.77% | 0.288 | 0.827 | 0.833 |
| e-means: massa sì, rianimazione sì, medie finali no | +1.38% | 0.555 | 0.932 | 0.926 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +1.25% | 0.558 | 0.933 | 0.928 |
| e-means: massa sì, rianimazione no, medie finali sì | +53.27% | 0.287 | 0.618 | 0.653 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +17.77% | 0.287 | 0.827 | 0.833 |
| e-means: massa sì, rianimazione no, medie finali no | +1.36% | 0.555 | 0.932 | 0.926 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +1.25% | 0.558 | 0.933 | 0.928 |
| mini-batch k-means dalle dimensioni delle liste | +1.27% | 0.555 | 0.932 | 0.925 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +1.20% | 0.560 | 0.933 | 0.927 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +3.22% | 0.546 | 0.928 | 0.924 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +2.45% | 0.556 | 0.933 | 0.931 |
| a caldo, 1 epoca a giro | +3.08% | 0.534 | 0.927 | 0.926 |
| a caldo, 3 epoche a giro | +0.53% | 0.578 | 0.936 | 0.934 |
| a caldo con massa a regime, 3 epoche a giro | +0.20% | 0.585 | 0.937 | 0.936 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.30% | 0.583 | 0.937 | 0.935 |
| da zero, 1 epoca | +3.80% | 0.525 | 0.923 | 0.922 |
| da zero, 3 epoche | +0.68% | 0.578 | 0.937 | 0.936 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.584 | 0.939 | 0.938 |

### Dopo 10 giri (indice fino al 2021-09-01; 2900 interrogazioni, di cui 1511 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +4.25% | 0.536 | 0.919 | 0.901 |
| e-means di Faiss 1.16.0, impostazioni di serie | +200.53% | 0.032 | 0.069 | 0.086 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +23.24% | 0.232 | 0.741 | 0.757 |
| e-means: massa no, rianimazione sì, medie finali sì | +198.61% | 0.033 | 0.071 | 0.087 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +23.11% | 0.238 | 0.755 | 0.766 |
| e-means: massa no, rianimazione sì, medie finali no | +190.77% | 0.026 | 0.062 | 0.075 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +23.70% | 0.241 | 0.732 | 0.747 |
| e-means: massa no, rianimazione no, medie finali sì | +119.20% | 0.047 | 0.226 | 0.257 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +31.41% | 0.083 | 0.446 | 0.466 |
| e-means: massa no, rianimazione no, medie finali no | +117.34% | 0.048 | 0.225 | 0.262 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +31.96% | 0.081 | 0.453 | 0.475 |
| e-means: massa sì, rianimazione sì, medie finali sì | +59.19% | 0.225 | 0.562 | 0.615 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +18.45% | 0.243 | 0.822 | 0.829 |
| e-means: massa sì, rianimazione sì, medie finali no | +2.29% | 0.548 | 0.931 | 0.922 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +1.97% | 0.556 | 0.935 | 0.929 |
| e-means: massa sì, rianimazione no, medie finali sì | +59.09% | 0.225 | 0.562 | 0.614 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +18.42% | 0.241 | 0.822 | 0.829 |
| e-means: massa sì, rianimazione no, medie finali no | +2.24% | 0.548 | 0.931 | 0.922 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +1.97% | 0.556 | 0.935 | 0.929 |
| mini-batch k-means dalle dimensioni delle liste | +2.16% | 0.548 | 0.930 | 0.921 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +1.96% | 0.554 | 0.934 | 0.926 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +4.24% | 0.541 | 0.927 | 0.921 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +2.95% | 0.561 | 0.937 | 0.933 |
| a caldo, 1 epoca a giro | +2.46% | 0.560 | 0.934 | 0.934 |
| a caldo, 3 epoche a giro | +0.30% | 0.600 | 0.943 | 0.942 |
| a caldo con massa a regime, 3 epoche a giro | +0.21% | 0.600 | 0.943 | 0.942 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.21% | 0.602 | 0.943 | 0.943 |
| da zero, 1 epoca | +3.05% | 0.556 | 0.934 | 0.934 |
| da zero, 3 epoche | +0.47% | 0.598 | 0.943 | 0.943 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.605 | 0.945 | 0.946 |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) | +2.04% | 0.581 | 0.940 | — |
