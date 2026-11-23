Insieme di dati: news-bge, 768 dimensioni.
Indice iniziale: 100000 testi, dal 2012-01-28 al 2015-02-08.
10 giri da 10000 testi, fino al 2019-09-01. 2048 liste, 3 seed dell'algoritmo.
Recall@10 leggendo lo 0,1% e l'1% dell'indice. Mediana su 3 seed. Gli intervalli sono in results/SINTESI.md.


### Dopo 1 giro (indice fino al 2015-06-06; 1536 interrogazioni, di cui 146 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +0.84% | 0.428 | 0.792 | 0.768 |
| e-means di Faiss 1.16.0, impostazioni di serie | +118.80% | 0.041 | 0.114 | 0.218 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +26.96% | 0.076 | 0.332 | 0.445 |
| e-means: massa no, rianimazione sì, medie finali sì | +117.38% | 0.044 | 0.115 | 0.228 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +26.97% | 0.081 | 0.337 | 0.442 |
| e-means: massa no, rianimazione sì, medie finali no | +119.69% | 0.031 | 0.097 | 0.199 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +27.90% | 0.089 | 0.352 | 0.447 |
| e-means: massa no, rianimazione no, medie finali sì | +93.31% | 0.084 | 0.186 | 0.292 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +23.90% | 0.099 | 0.364 | 0.431 |
| e-means: massa no, rianimazione no, medie finali no | +93.56% | 0.084 | 0.183 | 0.284 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +24.52% | 0.099 | 0.356 | 0.428 |
| e-means: massa sì, rianimazione sì, medie finali sì | +27.66% | 0.314 | 0.622 | 0.668 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +11.40% | 0.310 | 0.701 | 0.710 |
| e-means: massa sì, rianimazione sì, medie finali no | +0.62% | 0.430 | 0.792 | 0.771 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +0.60% | 0.431 | 0.792 | 0.773 |
| e-means: massa sì, rianimazione no, medie finali sì | +27.65% | 0.314 | 0.622 | 0.668 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +11.43% | 0.310 | 0.701 | 0.710 |
| e-means: massa sì, rianimazione no, medie finali no | +0.61% | 0.430 | 0.792 | 0.771 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +0.60% | 0.431 | 0.792 | 0.773 |
| mini-batch k-means dalle dimensioni delle liste | +0.58% | 0.430 | 0.793 | 0.772 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +0.57% | 0.430 | 0.793 | 0.773 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +1.32% | 0.428 | 0.792 | 0.765 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +1.19% | 0.432 | 0.792 | 0.771 |
| a caldo, 1 epoca a giro | +4.11% | 0.375 | 0.760 | 0.744 |
| a caldo, 3 epoche a giro | +0.64% | 0.430 | 0.789 | 0.768 |
| a caldo con massa a regime, 3 epoche a giro | +0.35% | 0.438 | 0.793 | 0.772 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.48% | 0.437 | 0.792 | 0.773 |
| da zero, 1 epoca | +4.77% | 0.376 | 0.757 | 0.752 |
| da zero, 3 epoche | +1.01% | 0.425 | 0.787 | 0.773 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.444 | 0.798 | 0.775 |

### Dopo 5 giri (indice fino al 2016-09-10; 2136 interrogazioni, di cui 746 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +3.98% | 0.404 | 0.773 | 0.718 |
| e-means di Faiss 1.16.0, impostazioni di serie | +138.54% | 0.026 | 0.061 | 0.124 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +26.26% | 0.111 | 0.396 | 0.510 |
| e-means: massa no, rianimazione sì, medie finali sì | +138.75% | 0.027 | 0.062 | 0.119 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +25.93% | 0.109 | 0.411 | 0.531 |
| e-means: massa no, rianimazione sì, medie finali no | +131.06% | 0.022 | 0.056 | 0.108 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +26.12% | 0.116 | 0.418 | 0.513 |
| e-means: massa no, rianimazione no, medie finali sì | +97.48% | 0.027 | 0.127 | 0.228 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +31.60% | 0.038 | 0.173 | 0.245 |
| e-means: massa no, rianimazione no, medie finali no | +97.54% | 0.028 | 0.129 | 0.230 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +32.04% | 0.037 | 0.174 | 0.241 |
| e-means: massa sì, rianimazione sì, medie finali sì | +58.79% | 0.155 | 0.388 | 0.530 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +20.35% | 0.169 | 0.536 | 0.624 |
| e-means: massa sì, rianimazione sì, medie finali no | +2.18% | 0.420 | 0.788 | 0.752 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +1.93% | 0.425 | 0.793 | 0.763 |
| e-means: massa sì, rianimazione no, medie finali sì | +58.58% | 0.157 | 0.391 | 0.529 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +20.24% | 0.168 | 0.537 | 0.623 |
| e-means: massa sì, rianimazione no, medie finali no | +2.14% | 0.419 | 0.789 | 0.752 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +1.93% | 0.425 | 0.793 | 0.763 |
| mini-batch k-means dalle dimensioni delle liste | +2.07% | 0.420 | 0.788 | 0.748 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +1.91% | 0.424 | 0.793 | 0.759 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +3.84% | 0.417 | 0.789 | 0.767 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +2.81% | 0.429 | 0.797 | 0.786 |
| a caldo, 1 epoca a giro | +3.29% | 0.417 | 0.785 | 0.784 |
| a caldo, 3 epoche a giro | +0.56% | 0.457 | 0.807 | 0.806 |
| a caldo con massa a regime, 3 epoche a giro | +0.23% | 0.470 | 0.811 | 0.808 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.37% | 0.466 | 0.812 | 0.806 |
| da zero, 1 epoca | +4.35% | 0.403 | 0.781 | 0.786 |
| da zero, 3 epoche | +0.73% | 0.456 | 0.808 | 0.810 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.475 | 0.814 | 0.817 |

### Dopo 10 giri (indice fino al 2019-09-01; 2898 interrogazioni, di cui 1508 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +6.95% | 0.376 | 0.745 | 0.682 |
| e-means di Faiss 1.16.0, impostazioni di serie | +136.03% | 0.022 | 0.049 | 0.077 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +30.53% | 0.115 | 0.388 | 0.484 |
| e-means: massa no, rianimazione sì, medie finali sì | +135.57% | 0.021 | 0.047 | 0.075 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +30.88% | 0.115 | 0.385 | 0.475 |
| e-means: massa no, rianimazione sì, medie finali no | +128.24% | 0.019 | 0.045 | 0.071 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +29.76% | 0.121 | 0.390 | 0.492 |
| e-means: massa no, rianimazione no, medie finali sì | +91.29% | 0.025 | 0.103 | 0.148 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +35.32% | 0.040 | 0.148 | 0.166 |
| e-means: massa no, rianimazione no, medie finali no | +92.90% | 0.026 | 0.102 | 0.143 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +35.66% | 0.038 | 0.134 | 0.153 |
| e-means: massa sì, rianimazione sì, medie finali sì | +61.42% | 0.118 | 0.364 | 0.476 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +23.53% | 0.137 | 0.512 | 0.572 |
| e-means: massa sì, rianimazione sì, medie finali no | +3.52% | 0.400 | 0.773 | 0.729 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +2.93% | 0.411 | 0.786 | 0.749 |
| e-means: massa sì, rianimazione no, medie finali sì | +61.34% | 0.117 | 0.365 | 0.477 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +23.47% | 0.138 | 0.504 | 0.569 |
| e-means: massa sì, rianimazione no, medie finali no | +3.43% | 0.399 | 0.773 | 0.727 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +2.99% | 0.409 | 0.783 | 0.744 |
| mini-batch k-means dalle dimensioni delle liste | +3.36% | 0.396 | 0.770 | 0.723 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +3.04% | 0.405 | 0.780 | 0.738 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +5.26% | 0.400 | 0.776 | 0.741 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +3.54% | 0.421 | 0.794 | 0.771 |
| a caldo, 1 epoca a giro | +2.69% | 0.441 | 0.797 | 0.792 |
| a caldo, 3 epoche a giro | +0.39% | 0.476 | 0.815 | 0.811 |
| a caldo con massa a regime, 3 epoche a giro | +0.05% | 0.487 | 0.819 | 0.810 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.13% | 0.489 | 0.820 | 0.813 |
| da zero, 1 epoca | +3.39% | 0.427 | 0.792 | 0.787 |
| da zero, 3 epoche | +0.59% | 0.476 | 0.814 | 0.810 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.487 | 0.822 | 0.819 |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) | +2.06% | 0.456 | 0.807 | — |
