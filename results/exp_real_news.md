Insieme di dati: news, 384 dimensioni.
Indice iniziale: 100000 testi, dal 2012-01-28 al 2015-02-08.
10 giri da 10000 testi, fino al 2019-09-01. 2048 liste, 3 seed dell'algoritmo.
Recall@10 leggendo lo 0,1% e l'1% dell'indice. Mediana su 3 seed. Gli intervalli sono in results/SINTESI.md.


### Dopo 1 giro (indice fino al 2015-06-06; 1536 interrogazioni, di cui 146 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +0.76% | 0.487 | 0.828 | 0.807 |
| e-means di Faiss 1.16.0, impostazioni di serie | +119.61% | 0.061 | 0.144 | 0.259 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +28.92% | 0.120 | 0.416 | 0.512 |
| e-means: massa no, rianimazione sì, medie finali sì | +117.65% | 0.065 | 0.154 | 0.247 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +28.58% | 0.125 | 0.430 | 0.537 |
| e-means: massa no, rianimazione sì, medie finali no | +121.55% | 0.047 | 0.131 | 0.232 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +29.51% | 0.133 | 0.440 | 0.545 |
| e-means: massa no, rianimazione no, medie finali sì | +91.85% | 0.121 | 0.251 | 0.323 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +25.92% | 0.149 | 0.451 | 0.527 |
| e-means: massa no, rianimazione no, medie finali no | +92.22% | 0.119 | 0.248 | 0.319 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +26.69% | 0.147 | 0.446 | 0.521 |
| e-means: massa sì, rianimazione sì, medie finali sì | +26.94% | 0.372 | 0.680 | 0.716 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +12.91% | 0.372 | 0.747 | 0.757 |
| e-means: massa sì, rianimazione sì, medie finali no | +0.57% | 0.487 | 0.828 | 0.809 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +0.55% | 0.489 | 0.827 | 0.806 |
| e-means: massa sì, rianimazione no, medie finali sì | +26.94% | 0.372 | 0.679 | 0.715 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +12.93% | 0.372 | 0.746 | 0.757 |
| e-means: massa sì, rianimazione no, medie finali no | +0.56% | 0.487 | 0.828 | 0.809 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +0.55% | 0.489 | 0.827 | 0.806 |
| mini-batch k-means dalle dimensioni delle liste | +0.53% | 0.488 | 0.827 | 0.808 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +0.52% | 0.489 | 0.828 | 0.806 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +1.28% | 0.483 | 0.825 | 0.805 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +1.15% | 0.485 | 0.824 | 0.804 |
| a caldo, 1 epoca a giro | +4.14% | 0.440 | 0.798 | 0.772 |
| a caldo, 3 epoche a giro | +0.60% | 0.490 | 0.826 | 0.806 |
| a caldo con massa a regime, 3 epoche a giro | +0.23% | 0.491 | 0.828 | 0.805 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.36% | 0.491 | 0.828 | 0.804 |
| da zero, 1 epoca | +4.98% | 0.429 | 0.798 | 0.779 |
| da zero, 3 epoche | +0.94% | 0.485 | 0.825 | 0.808 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.501 | 0.834 | 0.817 |

### Dopo 5 giri (indice fino al 2016-09-10; 2136 interrogazioni, di cui 746 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +3.19% | 0.461 | 0.806 | 0.758 |
| e-means di Faiss 1.16.0, impostazioni di serie | +146.77% | 0.032 | 0.070 | 0.129 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +28.29% | 0.147 | 0.464 | 0.547 |
| e-means: massa no, rianimazione sì, medie finali sì | +146.55% | 0.032 | 0.072 | 0.136 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +28.39% | 0.134 | 0.468 | 0.552 |
| e-means: massa no, rianimazione sì, medie finali no | +135.81% | 0.028 | 0.067 | 0.118 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +28.74% | 0.144 | 0.473 | 0.552 |
| e-means: massa no, rianimazione no, medie finali sì | +102.49% | 0.044 | 0.163 | 0.252 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +33.97% | 0.064 | 0.252 | 0.325 |
| e-means: massa no, rianimazione no, medie finali no | +102.05% | 0.045 | 0.160 | 0.255 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +33.84% | 0.062 | 0.249 | 0.313 |
| e-means: massa sì, rianimazione sì, medie finali sì | +59.29% | 0.189 | 0.438 | 0.571 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +22.33% | 0.198 | 0.577 | 0.643 |
| e-means: massa sì, rianimazione sì, medie finali no | +1.86% | 0.473 | 0.819 | 0.787 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +1.62% | 0.479 | 0.822 | 0.794 |
| e-means: massa sì, rianimazione no, medie finali sì | +59.39% | 0.189 | 0.435 | 0.570 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +22.29% | 0.198 | 0.576 | 0.647 |
| e-means: massa sì, rianimazione no, medie finali no | +1.79% | 0.473 | 0.819 | 0.787 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +1.62% | 0.479 | 0.822 | 0.792 |
| mini-batch k-means dalle dimensioni delle liste | +1.73% | 0.474 | 0.817 | 0.783 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +1.60% | 0.478 | 0.819 | 0.788 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +3.47% | 0.470 | 0.818 | 0.790 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +2.58% | 0.479 | 0.823 | 0.799 |
| a caldo, 1 epoca a giro | +3.25% | 0.467 | 0.811 | 0.797 |
| a caldo, 3 epoche a giro | +0.53% | 0.510 | 0.834 | 0.823 |
| a caldo con massa a regime, 3 epoche a giro | +0.24% | 0.512 | 0.834 | 0.819 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.33% | 0.511 | 0.835 | 0.821 |
| da zero, 1 epoca | +4.15% | 0.456 | 0.810 | 0.801 |
| da zero, 3 epoche | +0.80% | 0.507 | 0.833 | 0.819 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.524 | 0.840 | 0.832 |

### Dopo 10 giri (indice fino al 2019-09-01; 2898 interrogazioni, di cui 1508 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +5.61% | 0.429 | 0.781 | 0.728 |
| e-means di Faiss 1.16.0, impostazioni di serie | +145.10% | 0.024 | 0.052 | 0.079 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +32.87% | 0.140 | 0.433 | 0.503 |
| e-means: massa no, rianimazione sì, medie finali sì | +143.66% | 0.024 | 0.053 | 0.080 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +32.81% | 0.142 | 0.448 | 0.514 |
| e-means: massa no, rianimazione sì, medie finali no | +135.27% | 0.021 | 0.048 | 0.070 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +31.60% | 0.144 | 0.449 | 0.526 |
| e-means: massa no, rianimazione no, medie finali sì | +98.63% | 0.035 | 0.143 | 0.196 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +37.21% | 0.064 | 0.220 | 0.245 |
| e-means: massa no, rianimazione no, medie finali no | +100.63% | 0.036 | 0.142 | 0.192 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +37.19% | 0.065 | 0.233 | 0.258 |
| e-means: massa sì, rianimazione sì, medie finali sì | +62.74% | 0.139 | 0.409 | 0.509 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +25.18% | 0.164 | 0.550 | 0.603 |
| e-means: massa sì, rianimazione sì, medie finali no | +2.96% | 0.452 | 0.807 | 0.770 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +2.53% | 0.459 | 0.812 | 0.779 |
| e-means: massa sì, rianimazione no, medie finali sì | +62.47% | 0.139 | 0.412 | 0.512 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +25.41% | 0.158 | 0.546 | 0.598 |
| e-means: massa sì, rianimazione no, medie finali no | +2.90% | 0.451 | 0.807 | 0.768 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +2.56% | 0.458 | 0.811 | 0.777 |
| mini-batch k-means dalle dimensioni delle liste | +2.84% | 0.451 | 0.805 | 0.764 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +2.59% | 0.457 | 0.810 | 0.773 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +4.87% | 0.450 | 0.807 | 0.776 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +3.30% | 0.468 | 0.818 | 0.795 |
| a caldo, 1 epoca a giro | +2.64% | 0.493 | 0.824 | 0.812 |
| a caldo, 3 epoche a giro | +0.34% | 0.531 | 0.840 | 0.829 |
| a caldo con massa a regime, 3 epoche a giro | +0.09% | 0.534 | 0.840 | 0.828 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.14% | 0.533 | 0.838 | 0.825 |
| da zero, 1 epoca | +3.33% | 0.479 | 0.822 | 0.811 |
| da zero, 3 epoche | +0.58% | 0.526 | 0.838 | 0.828 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.536 | 0.843 | 0.835 |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) | +1.99% | 0.504 | 0.831 | — |
