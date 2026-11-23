Insieme di dati: arxiv-bge, 768 dimensioni.
Indice iniziale: 100000 testi, dal 2007-04-01 al 2016-08-01.
10 giri da 10000 testi, fino al 2021-09-01. 2048 liste, 3 seed dell'algoritmo.
Recall@10 leggendo lo 0,1% e l'1% dell'indice. Mediana su 3 seed. Gli intervalli sono in results/SINTESI.md.


### Dopo 1 giro (indice fino al 2017-04-01; 1534 interrogazioni, di cui 145 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +0.64% | 0.565 | 0.937 | 0.943 |
| e-means di Faiss 1.16.0, impostazioni di serie | +137.16% | 0.077 | 0.223 | 0.272 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +25.68% | 0.160 | 0.654 | 0.671 |
| e-means: massa no, rianimazione sì, medie finali sì | +139.43% | 0.084 | 0.234 | 0.267 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +25.05% | 0.171 | 0.665 | 0.682 |
| e-means: massa no, rianimazione sì, medie finali no | +155.24% | 0.061 | 0.184 | 0.221 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +25.96% | 0.190 | 0.678 | 0.688 |
| e-means: massa no, rianimazione no, medie finali sì | +88.78% | 0.133 | 0.371 | 0.381 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +23.78% | 0.162 | 0.670 | 0.664 |
| e-means: massa no, rianimazione no, medie finali no | +89.20% | 0.132 | 0.377 | 0.389 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +24.61% | 0.159 | 0.660 | 0.659 |
| e-means: massa sì, rianimazione sì, medie finali sì | +25.87% | 0.448 | 0.831 | 0.834 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +15.72% | 0.442 | 0.892 | 0.894 |
| e-means: massa sì, rianimazione sì, medie finali no | +0.46% | 0.567 | 0.937 | 0.943 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +0.44% | 0.568 | 0.937 | 0.943 |
| e-means: massa sì, rianimazione no, medie finali sì | +25.85% | 0.448 | 0.831 | 0.834 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +15.72% | 0.442 | 0.892 | 0.894 |
| e-means: massa sì, rianimazione no, medie finali no | +0.45% | 0.567 | 0.937 | 0.943 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +0.44% | 0.568 | 0.937 | 0.943 |
| mini-batch k-means dalle dimensioni delle liste | +0.42% | 0.567 | 0.937 | 0.942 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +0.41% | 0.568 | 0.937 | 0.943 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +1.26% | 0.563 | 0.936 | 0.941 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +1.15% | 0.565 | 0.937 | 0.942 |
| a caldo, 1 epoca a giro | +3.90% | 0.515 | 0.925 | 0.926 |
| a caldo, 3 epoche a giro | +0.52% | 0.568 | 0.938 | 0.941 |
| a caldo con massa a regime, 3 epoche a giro | +0.19% | 0.573 | 0.937 | 0.939 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.31% | 0.571 | 0.935 | 0.934 |
| da zero, 1 epoca | +4.38% | 0.508 | 0.922 | 0.923 |
| da zero, 3 epoche | +0.73% | 0.561 | 0.937 | 0.930 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.582 | 0.938 | 0.941 |

### Dopo 5 giri (indice fino al 2019-07-01; 2145 interrogazioni, di cui 756 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +2.29% | 0.560 | 0.934 | 0.928 |
| e-means di Faiss 1.16.0, impostazioni di serie | +210.34% | 0.038 | 0.083 | 0.106 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +23.05% | 0.206 | 0.750 | 0.756 |
| e-means: massa no, rianimazione sì, medie finali sì | +208.67% | 0.036 | 0.081 | 0.105 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +22.49% | 0.214 | 0.763 | 0.766 |
| e-means: massa no, rianimazione sì, medie finali no | +198.08% | 0.030 | 0.068 | 0.086 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +23.37% | 0.231 | 0.751 | 0.758 |
| e-means: massa no, rianimazione no, medie finali sì | +107.60% | 0.051 | 0.233 | 0.272 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +30.63% | 0.076 | 0.456 | 0.482 |
| e-means: massa no, rianimazione no, medie finali no | +107.70% | 0.050 | 0.238 | 0.277 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +30.75% | 0.073 | 0.445 | 0.464 |
| e-means: massa sì, rianimazione sì, medie finali sì | +51.00% | 0.281 | 0.619 | 0.665 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +17.42% | 0.287 | 0.840 | 0.844 |
| e-means: massa sì, rianimazione sì, medie finali no | +1.36% | 0.567 | 0.937 | 0.935 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +1.21% | 0.572 | 0.938 | 0.937 |
| e-means: massa sì, rianimazione no, medie finali sì | +51.31% | 0.282 | 0.619 | 0.667 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +17.43% | 0.286 | 0.839 | 0.843 |
| e-means: massa sì, rianimazione no, medie finali no | +1.32% | 0.567 | 0.937 | 0.935 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +1.21% | 0.572 | 0.938 | 0.937 |
| mini-batch k-means dalle dimensioni delle liste | +1.23% | 0.567 | 0.937 | 0.934 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +1.16% | 0.571 | 0.938 | 0.936 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +3.11% | 0.558 | 0.933 | 0.930 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +2.43% | 0.569 | 0.937 | 0.937 |
| a caldo, 1 epoca a giro | +3.16% | 0.547 | 0.930 | 0.928 |
| a caldo, 3 epoche a giro | +0.49% | 0.585 | 0.940 | 0.942 |
| a caldo con massa a regime, 3 epoche a giro | +0.15% | 0.600 | 0.942 | 0.941 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.22% | 0.592 | 0.942 | 0.943 |
| da zero, 1 epoca | +3.83% | 0.532 | 0.929 | 0.928 |
| da zero, 3 epoche | +0.69% | 0.585 | 0.943 | 0.943 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.598 | 0.943 | 0.944 |

### Dopo 10 giri (indice fino al 2021-09-01; 2900 interrogazioni, di cui 1511 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall, 0,1% letto | Recall, 1% letto | Recall 1%, periodo aggiunto |
|---|---|---|---|---|
| mai aggiornare | +4.18% | 0.547 | 0.928 | 0.916 |
| e-means di Faiss 1.16.0, impostazioni di serie | +211.46% | 0.029 | 0.064 | 0.079 |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +22.46% | 0.236 | 0.772 | 0.787 |
| e-means: massa no, rianimazione sì, medie finali sì | +211.58% | 0.030 | 0.068 | 0.085 |
| e-means: massa no, rianimazione sì, medie finali sì + liste ricostruite | +22.29% | 0.238 | 0.773 | 0.780 |
| e-means: massa no, rianimazione sì, medie finali no | +205.19% | 0.025 | 0.057 | 0.072 |
| e-means: massa no, rianimazione sì, medie finali no + liste ricostruite | +23.42% | 0.235 | 0.756 | 0.763 |
| e-means: massa no, rianimazione no, medie finali sì | +114.40% | 0.043 | 0.223 | 0.265 |
| e-means: massa no, rianimazione no, medie finali sì + liste ricostruite | +31.76% | 0.067 | 0.416 | 0.443 |
| e-means: massa no, rianimazione no, medie finali no | +111.94% | 0.043 | 0.220 | 0.260 |
| e-means: massa no, rianimazione no, medie finali no + liste ricostruite | +31.97% | 0.066 | 0.417 | 0.443 |
| e-means: massa sì, rianimazione sì, medie finali sì | +56.68% | 0.223 | 0.571 | 0.633 |
| e-means: massa sì, rianimazione sì, medie finali sì + liste ricostruite | +18.11% | 0.241 | 0.830 | 0.838 |
| e-means: massa sì, rianimazione sì, medie finali no | +2.16% | 0.559 | 0.937 | 0.932 |
| e-means: massa sì, rianimazione sì, medie finali no + liste ricostruite | +1.84% | 0.569 | 0.940 | 0.936 |
| e-means: massa sì, rianimazione no, medie finali sì | +56.29% | 0.223 | 0.568 | 0.631 |
| e-means: massa sì, rianimazione no, medie finali sì + liste ricostruite | +18.10% | 0.236 | 0.831 | 0.835 |
| e-means: massa sì, rianimazione no, medie finali no | +2.13% | 0.559 | 0.938 | 0.932 |
| e-means: massa sì, rianimazione no, medie finali no + liste ricostruite | +1.87% | 0.568 | 0.940 | 0.937 |
| mini-batch k-means dalle dimensioni delle liste | +2.04% | 0.559 | 0.937 | 0.931 |
| mini-batch k-means dalle dimensioni delle liste + liste ricostruite | +1.85% | 0.566 | 0.939 | 0.935 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +4.02% | 0.551 | 0.931 | 0.926 |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali + liste ricostruite | +2.83% | 0.572 | 0.940 | 0.939 |
| a caldo, 1 epoca a giro | +2.42% | 0.574 | 0.938 | 0.940 |
| a caldo, 3 epoche a giro | +0.27% | 0.614 | 0.947 | 0.946 |
| a caldo con massa a regime, 3 epoche a giro | +0.10% | 0.614 | 0.947 | 0.947 |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.13% | 0.614 | 0.946 | 0.947 |
| da zero, 1 epoca | +2.93% | 0.566 | 0.937 | 0.938 |
| da zero, 3 epoche | +0.43% | 0.606 | 0.946 | 0.945 |
| da zero, 10 epoche (riferimento) | +0.00% | 0.619 | 0.948 | 0.948 |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) | +1.95% | 0.593 | 0.943 | — |
