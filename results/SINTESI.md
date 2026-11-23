# Sintesi dei risultati su dati veri

Generata da analyze.py. Metodo e limiti nel docstring di analyze.py e di exp_real.py.

## notizie HuffPost, all-MiniLM-L6-v2 (384 dimensioni)

Dopo 10 giri, indice da 200.000 testi, 2898 interrogazioni. Recall@10; tra parentesi quadre l'intervallo al 95%.

Periodo aggiunto: le 1508 interrogazioni datate dopo l'indice iniziale.

| Strategia | Errore nelle liste | Recall, 1% letto | Recall 1%, periodo aggiunto | Recall, 0,1% letto |
|---|---|---|---|---|
| mai aggiornare | +5.61% | 0.781 [0.773; 0.789] | 0.727 [0.715; 0.740] | 0.427 [0.417; 0.438] |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) | +1.99% | 0.830 [0.823; 0.837] | — | 0.504 [0.493; 0.514] |
| e-means di Faiss 1.16.0, impostazioni di serie | +145.10% | 0.052 [0.049; 0.056] | 0.079 [0.072; 0.086] | 0.024 [0.022; 0.027] |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +32.87% | 0.434 [0.425; 0.444] | 0.505 [0.490; 0.519] | 0.141 [0.135; 0.148] |
| mini-batch k-means dalle dimensioni delle liste | +2.84% | 0.804 [0.796; 0.812] | 0.765 [0.754; 0.777] | 0.448 [0.437; 0.458] |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +4.87% | 0.807 [0.799; 0.814] | 0.776 [0.765; 0.788] | 0.448 [0.438; 0.459] |
| e-means: massa sì, rianimazione no, medie finali no | +2.90% | 0.806 [0.798; 0.814] | 0.768 [0.757; 0.780] | 0.448 [0.438; 0.459] |
| da zero, 1 epoca | +3.33% | 0.821 [0.814; 0.828] | 0.810 [0.801; 0.820] | 0.479 [0.469; 0.489] |
| a caldo, 1 epoca a giro | +2.64% | 0.823 [0.816; 0.830] | 0.811 [0.801; 0.821] | 0.493 [0.482; 0.503] |
| da zero, 3 epoche | +0.58% | 0.839 [0.832; 0.845] | 0.829 [0.819; 0.839] | 0.525 [0.515; 0.535] |
| a caldo, 3 epoche a giro | +0.34% | 0.839 [0.832; 0.846] | 0.829 [0.820; 0.839] | 0.531 [0.521; 0.541] |
| a caldo con massa a regime, 3 epoche a giro | +0.09% | 0.840 [0.833; 0.847] | 0.827 [0.817; 0.836] | 0.533 [0.522; 0.543] |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.14% | 0.839 [0.832; 0.845] | 0.825 [0.816; 0.835] | 0.533 [0.522; 0.543] |
| da zero, 10 epoche (riferimento) | +0.00% | 0.843 [0.836; 0.849] | 0.835 [0.826; 0.845] | 0.536 [0.526; 0.547] |

Differenze appaiate di recall (1% letto), dopo 10 giri. L'ultima colonna è la stessa differenza calcolata seed per seed.

| Confronto | Differenza [intervallo sulle interrogazioni] | Lo zero è escluso? | Tra i seed [min; max] |
|---|---|---|---|
| da zero, 10 epoche (riferimento) − mai aggiornare | +0.062 [+0.056; +0.067] | sì | [+0.059; +0.064] |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) − mai aggiornare | +0.049 [+0.043; +0.054] | sì | [+0.048; +0.050] |
| mini-batch k-means dalle dimensioni delle liste − mai aggiornare | +0.023 [+0.020; +0.026] | sì | [+0.022; +0.026] |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali − mini-batch k-means dalle dimensioni delle liste | +0.003 [+0.000; +0.006] | sì | [-0.001; +0.006] |
| e-means: massa sì, rianimazione no, medie finali no − mini-batch k-means dalle dimensioni delle liste | +0.002 [+0.001; +0.003] | sì | [+0.001; +0.003] |
| da zero, 3 epoche − da zero, 10 epoche (riferimento) | -0.004 [-0.006; -0.002] | sì | [-0.006; -0.002] |
| a caldo, 3 epoche a giro − da zero, 3 epoche | +0.000 [-0.002; +0.003] | no | [-0.002; +0.002] |
| a caldo con massa a regime, 3 epoche a giro − da zero, 3 epoche | +0.001 [-0.001; +0.004] | no | [-0.004; +0.004] |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro − da zero, 3 epoche | -0.000 [-0.003; +0.003] | no | [-0.003; +0.002] |
| a caldo, 1 epoca a giro − da zero, 1 epoca | +0.002 [-0.001; +0.005] | no | [+0.002; +0.002] |
| da zero, 1 epoca − mai aggiornare | +0.040 [+0.034; +0.046] | sì | [+0.037; +0.043] |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite − mai aggiornare | -0.347 [-0.358; -0.336] | sì | [-0.351; -0.340] |
| e-means di Faiss 1.16.0, impostazioni di serie − e-means: massa no, rianimazione sì, medie finali sì | -0.001 [-0.002; +0.001] | no | [-0.002; +0.002] |

Scomposizione dell'uso ingenuo: e-means sui soli testi nuovi, dai centroidi vecchi. Recall con l'1% letto.

| Massa iniziale | Rianimazione | Medie finali | Dopo 1 giro | Dopo 10 giri | Dopo 10 giri, liste ricostruite |
|---|---|---|---|---|---|
| no | sì | sì | 0.153 [0.143; 0.163] | 0.053 [0.049; 0.057] | 0.448 [0.438; 0.458] |
| no | sì | no | 0.130 [0.122; 0.138] | 0.048 [0.044; 0.052] | 0.451 [0.441; 0.461] |
| no | no | sì | 0.250 [0.239; 0.262] | 0.143 [0.137; 0.150] | 0.227 [0.220; 0.235] |
| no | no | no | 0.249 [0.238; 0.260] | 0.142 [0.136; 0.149] | 0.229 [0.222; 0.237] |
| sì | sì | sì | 0.681 [0.669; 0.692] | 0.410 [0.400; 0.421] | 0.550 [0.540; 0.560] |
| sì | sì | no | 0.827 [0.817; 0.836] | 0.806 [0.798; 0.814] | 0.811 [0.804; 0.819] |
| sì | no | sì | 0.681 [0.669; 0.692] | 0.412 [0.402; 0.423] | 0.545 [0.534; 0.555] |
| sì | no | no | 0.827 [0.817; 0.836] | 0.806 [0.798; 0.814] | 0.811 [0.803; 0.818] |

Per confronto, dopo 10 giri: mai aggiornare 0.781; riferimento 0.843.

## abstract arXiv, all-MiniLM-L6-v2 (384 dimensioni)

Dopo 10 giri, indice da 200.000 testi, 2900 interrogazioni. Recall@10; tra parentesi quadre l'intervallo al 95%.

Periodo aggiunto: le 1511 interrogazioni datate dopo l'indice iniziale.

| Strategia | Errore nelle liste | Recall, 1% letto | Recall 1%, periodo aggiunto | Recall, 0,1% letto |
|---|---|---|---|---|
| mai aggiornare | +4.25% | 0.918 [0.914; 0.923] | 0.900 [0.893; 0.908] | 0.536 [0.526; 0.545] |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) | +2.04% | 0.939 [0.935; 0.942] | — | 0.579 [0.570; 0.588] |
| e-means di Faiss 1.16.0, impostazioni di serie | +200.53% | 0.069 [0.066; 0.072] | 0.086 [0.081; 0.091] | 0.033 [0.031; 0.035] |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +23.24% | 0.744 [0.737; 0.752] | 0.758 [0.747; 0.767] | 0.231 [0.225; 0.238] |
| mini-batch k-means dalle dimensioni delle liste | +2.16% | 0.930 [0.926; 0.934] | 0.921 [0.916; 0.927] | 0.548 [0.539; 0.558] |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +4.24% | 0.927 [0.923; 0.931] | 0.921 [0.916; 0.926] | 0.541 [0.532; 0.550] |
| e-means: massa sì, rianimazione no, medie finali no | +2.24% | 0.931 [0.927; 0.935] | 0.922 [0.917; 0.928] | 0.548 [0.538; 0.557] |
| da zero, 1 epoca | +3.05% | 0.934 [0.930; 0.938] | 0.935 [0.929; 0.939] | 0.555 [0.546; 0.563] |
| a caldo, 1 epoca a giro | +2.46% | 0.934 [0.931; 0.938] | 0.935 [0.930; 0.940] | 0.560 [0.551; 0.569] |
| da zero, 3 epoche | +0.47% | 0.943 [0.939; 0.947] | 0.943 [0.938; 0.948] | 0.600 [0.591; 0.609] |
| a caldo, 3 epoche a giro | +0.30% | 0.943 [0.940; 0.947] | 0.943 [0.938; 0.948] | 0.602 [0.593; 0.611] |
| a caldo con massa a regime, 3 epoche a giro | +0.21% | 0.943 [0.940; 0.947] | 0.942 [0.937; 0.946] | 0.601 [0.592; 0.611] |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.21% | 0.943 [0.940; 0.947] | 0.943 [0.938; 0.947] | 0.602 [0.592; 0.612] |
| da zero, 10 epoche (riferimento) | +0.00% | 0.945 [0.942; 0.949] | 0.946 [0.941; 0.950] | 0.605 [0.596; 0.614] |

Differenze appaiate di recall (1% letto), dopo 10 giri. L'ultima colonna è la stessa differenza calcolata seed per seed.

| Confronto | Differenza [intervallo sulle interrogazioni] | Lo zero è escluso? | Tra i seed [min; max] |
|---|---|---|---|
| da zero, 10 epoche (riferimento) − mai aggiornare | +0.027 [+0.024; +0.031] | sì | [+0.025; +0.031] |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) − mai aggiornare | +0.021 [+0.017; +0.024] | sì | [+0.020; +0.022] |
| mini-batch k-means dalle dimensioni delle liste − mai aggiornare | +0.012 [+0.010; +0.014] | sì | [+0.010; +0.014] |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali − mini-batch k-means dalle dimensioni delle liste | -0.003 [-0.005; -0.001] | sì | [-0.004; -0.001] |
| e-means: massa sì, rianimazione no, medie finali no − mini-batch k-means dalle dimensioni delle liste | +0.001 [-0.000; +0.001] | no | [-0.000; +0.001] |
| da zero, 3 epoche − da zero, 10 epoche (riferimento) | -0.002 [-0.004; -0.001] | sì | [-0.004; -0.001] |
| a caldo, 3 epoche a giro − da zero, 3 epoche | +0.000 [-0.002; +0.002] | no | [-0.000; +0.000] |
| a caldo con massa a regime, 3 epoche a giro − da zero, 3 epoche | +0.000 [-0.002; +0.002] | no | [-0.001; +0.001] |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro − da zero, 3 epoche | +0.000 [-0.001; +0.002] | no | [-0.001; +0.001] |
| a caldo, 1 epoca a giro − da zero, 1 epoca | +0.000 [-0.001; +0.002] | no | [-0.000; +0.001] |
| da zero, 1 epoca − mai aggiornare | +0.016 [+0.012; +0.020] | sì | [+0.013; +0.020] |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite − mai aggiornare | -0.174 [-0.181; -0.167] | sì | [-0.180; -0.167] |
| e-means di Faiss 1.16.0, impostazioni di serie − e-means: massa no, rianimazione sì, medie finali sì | -0.002 [-0.004; -0.000] | sì | [-0.003; +0.001] |

Scomposizione dell'uso ingenuo: e-means sui soli testi nuovi, dai centroidi vecchi. Recall con l'1% letto.

| Massa iniziale | Rianimazione | Medie finali | Dopo 1 giro | Dopo 10 giri | Dopo 10 giri, liste ricostruite |
|---|---|---|---|---|---|
| no | sì | sì | 0.232 [0.222; 0.241] | 0.071 [0.068; 0.074] | 0.755 [0.747; 0.762] |
| no | sì | no | 0.184 [0.176; 0.192] | 0.062 [0.059; 0.065] | 0.737 [0.729; 0.745] |
| no | no | sì | 0.390 [0.379; 0.401] | 0.227 [0.221; 0.233] | 0.445 [0.436; 0.453] |
| no | no | no | 0.392 [0.380; 0.403] | 0.227 [0.221; 0.233] | 0.445 [0.437; 0.454] |
| sì | sì | sì | 0.836 [0.827; 0.843] | 0.562 [0.553; 0.571] | 0.820 [0.814; 0.827] |
| sì | sì | no | 0.932 [0.926; 0.936] | 0.931 [0.927; 0.935] | 0.935 [0.931; 0.939] |
| sì | no | sì | 0.836 [0.827; 0.843] | 0.562 [0.553; 0.571] | 0.821 [0.815; 0.828] |
| sì | no | no | 0.932 [0.926; 0.936] | 0.931 [0.927; 0.935] | 0.935 [0.931; 0.939] |

Per confronto, dopo 10 giri: mai aggiornare 0.918; riferimento 0.945.

## notizie HuffPost, bge-base-en-v1.5 (768 dimensioni)

Risultati mancanti.

## abstract arXiv, bge-base-en-v1.5 (768 dimensioni)

Risultati mancanti.
