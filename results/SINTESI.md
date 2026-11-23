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

Addestramento dei centroidi sui 200.000 testi, implementazioni di Faiss (mediana di 6 ripetizioni; la riassegnazione dei vettori non è compresa nel tempo):

| Metodo | Passate | Tempo | Errore di addestramento | Errore sui testi tenuti fuori | Recall, 1% letto |
|---|---|---|---|---|---|
| e-means | 1 | 1.5 s | 0.6268 | 0.6395 | 0.818 |
| e-means | 2 | 2.9 s | 0.6128 | 0.6293 | 0.836 |
| e-means | 3 | 4.3 s | 0.6099 | 0.6270 | 0.838 |
| e-means | 5 | 7.1 s | 0.6080 | 0.6252 | 0.840 |
| e-means | 10 | 14.1 s | 0.6066 | 0.6237 | 0.842 |
| k-means | 3 | 2.7 s | 0.6264 | 0.6414 | 0.833 |
| k-means | 5 | 4.5 s | 0.6192 | 0.6351 | 0.838 |
| k-means | 10 | 9.1 s | 0.6136 | 0.6305 | 0.842 |
| k-means | 12 | 10.9 s | 0.6127 | 0.6299 | 0.843 |
| k-means | 15 | 13.6 s | 0.6119 | 0.6293 | 0.843 |
| k-means | 20 | 18.2 s | 0.6112 | 0.6288 | 0.843 |
| k-means | 25 | 22.6 s | 0.6109 | 0.6285 | 0.843 |

A parità di errore di addestramento: il k-means non raggiunge e-means a 3 epoche nemmeno con 25 iterazioni (22.6 s contro 4.3 s): rapporto dei tempi superiore a 5.3.

A parità di errore sui testi tenuti fuori: il k-means non raggiunge e-means a 3 epoche nemmeno con 25 iterazioni (22.6 s contro 4.3 s): rapporto dei tempi superiore a 5.3.

A parità di recall con lo 0,1% dell'indice letto: al k-means servono tra 15 e 20 iterazioni, cioè tra 13.6 e 18.2 s contro 4.3 s di e-means a 3 epoche: rapporto dei tempi tra 3.2 e 4.2.

A parità di recall con l'1% dell'indice letto: al k-means servono tra 3 e 5 iterazioni, cioè tra 2.7 e 4.5 s contro 4.3 s di e-means a 3 epoche: rapporto dei tempi tra 0.6 e 1.1.

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

Addestramento dei centroidi sui 200.000 testi, implementazioni di Faiss (mediana di 6 ripetizioni; la riassegnazione dei vettori non è compresa nel tempo):

| Metodo | Passate | Tempo | Errore di addestramento | Errore sui testi tenuti fuori | Recall, 1% letto |
|---|---|---|---|---|---|
| e-means | 1 | 1.5 s | 0.5181 | 0.5278 | 0.933 |
| e-means | 2 | 2.9 s | 0.5075 | 0.5202 | 0.940 |
| e-means | 3 | 4.3 s | 0.5053 | 0.5177 | 0.943 |
| e-means | 5 | 7.1 s | 0.5039 | 0.5174 | 0.945 |
| e-means | 10 | 14.1 s | 0.5029 | 0.5164 | 0.945 |
| k-means | 3 | 2.7 s | 0.5180 | 0.5293 | 0.936 |
| k-means | 5 | 4.5 s | 0.5126 | 0.5247 | 0.940 |
| k-means | 10 | 9.1 s | 0.5083 | 0.5213 | 0.943 |
| k-means | 12 | 10.9 s | 0.5076 | 0.5206 | 0.944 |
| k-means | 15 | 13.6 s | 0.5070 | 0.5199 | 0.944 |
| k-means | 20 | 18.2 s | 0.5064 | 0.5194 | 0.944 |
| k-means | 25 | 22.7 s | 0.5061 | 0.5191 | 0.944 |

A parità di errore di addestramento: il k-means non raggiunge e-means a 3 epoche nemmeno con 25 iterazioni (22.7 s contro 4.3 s): rapporto dei tempi superiore a 5.3.

A parità di errore sui testi tenuti fuori: il k-means non raggiunge e-means a 3 epoche nemmeno con 25 iterazioni (22.7 s contro 4.3 s): rapporto dei tempi superiore a 5.3.

A parità di recall con lo 0,1% dell'indice letto: al k-means servono tra 12 e 15 iterazioni, cioè tra 10.9 e 13.6 s contro 4.3 s di e-means a 3 epoche: rapporto dei tempi tra 2.5 e 3.2.

A parità di recall con l'1% dell'indice letto: al k-means servono tra 5 e 10 iterazioni, cioè tra 4.5 e 9.1 s contro 4.3 s di e-means a 3 epoche: rapporto dei tempi tra 1.1 e 2.1.

## notizie HuffPost, bge-base-en-v1.5 (768 dimensioni)

Dopo 10 giri, indice da 200.000 testi, 2898 interrogazioni. Recall@10; tra parentesi quadre l'intervallo al 95%.

Periodo aggiunto: le 1508 interrogazioni datate dopo l'indice iniziale.

| Strategia | Errore nelle liste | Recall, 1% letto | Recall 1%, periodo aggiunto | Recall, 0,1% letto |
|---|---|---|---|---|
| mai aggiornare | +6.95% | 0.746 [0.738; 0.755] | 0.684 [0.672; 0.695] | 0.375 [0.365; 0.385] |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) | +2.06% | 0.807 [0.800; 0.814] | — | 0.458 [0.448; 0.467] |
| e-means di Faiss 1.16.0, impostazioni di serie | +136.03% | 0.049 [0.046; 0.053] | 0.078 [0.072; 0.085] | 0.022 [0.019; 0.024] |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite | +30.53% | 0.389 [0.379; 0.399] | 0.486 [0.472; 0.501] | 0.116 [0.111; 0.123] |
| mini-batch k-means dalle dimensioni delle liste | +3.36% | 0.770 [0.762; 0.778] | 0.722 [0.710; 0.733] | 0.397 [0.387; 0.407] |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali | +5.26% | 0.775 [0.767; 0.783] | 0.740 [0.730; 0.751] | 0.402 [0.392; 0.411] |
| e-means: massa sì, rianimazione no, medie finali no | +3.43% | 0.773 [0.765; 0.781] | 0.727 [0.716; 0.739] | 0.399 [0.389; 0.409] |
| da zero, 1 epoca | +3.39% | 0.793 [0.786; 0.800] | 0.785 [0.775; 0.795] | 0.426 [0.416; 0.435] |
| a caldo, 1 epoca a giro | +2.69% | 0.798 [0.790; 0.805] | 0.793 [0.783; 0.802] | 0.441 [0.432; 0.451] |
| da zero, 3 epoche | +0.59% | 0.814 [0.807; 0.821] | 0.810 [0.800; 0.819] | 0.475 [0.465; 0.485] |
| a caldo, 3 epoche a giro | +0.39% | 0.815 [0.808; 0.822] | 0.811 [0.802; 0.820] | 0.477 [0.467; 0.487] |
| a caldo con massa a regime, 3 epoche a giro | +0.05% | 0.819 [0.812; 0.826] | 0.811 [0.801; 0.820] | 0.489 [0.479; 0.499] |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro | +0.13% | 0.820 [0.813; 0.827] | 0.814 [0.805; 0.823] | 0.489 [0.479; 0.500] |
| da zero, 10 epoche (riferimento) | +0.00% | 0.821 [0.814; 0.828] | 0.819 [0.809; 0.828] | 0.487 [0.477; 0.497] |

Differenze appaiate di recall (1% letto), dopo 10 giri. L'ultima colonna è la stessa differenza calcolata seed per seed.

| Confronto | Differenza [intervallo sulle interrogazioni] | Lo zero è escluso? | Tra i seed [min; max] |
|---|---|---|---|
| da zero, 10 epoche (riferimento) − mai aggiornare | +0.075 [+0.068; +0.081] | sì | [+0.071; +0.078] |
| mai aggiornare, testi in ordine casuale (controllo senza deriva) − mai aggiornare | +0.061 [+0.054; +0.067] | sì | [+0.057; +0.063] |
| mini-batch k-means dalle dimensioni delle liste − mai aggiornare | +0.024 [+0.020; +0.028] | sì | [+0.019; +0.028] |
| e-means: massa 0,2, passo/4, senza rianimazione né medie finali − mini-batch k-means dalle dimensioni delle liste | +0.005 [+0.001; +0.008] | sì | [+0.003; +0.006] |
| e-means: massa sì, rianimazione no, medie finali no − mini-batch k-means dalle dimensioni delle liste | +0.003 [+0.001; +0.004] | sì | [+0.003; +0.003] |
| da zero, 3 epoche − da zero, 10 epoche (riferimento) | -0.007 [-0.009; -0.004] | sì | [-0.011; -0.002] |
| a caldo, 3 epoche a giro − da zero, 3 epoche | +0.001 [-0.001; +0.003] | no | [-0.001; +0.002] |
| a caldo con massa a regime, 3 epoche a giro − da zero, 3 epoche | +0.005 [+0.002; +0.008] | sì | [+0.004; +0.006] |
| a caldo con massa a regime, senza medie finali, 3 epoche a giro − da zero, 3 epoche | +0.006 [+0.003; +0.009] | sì | [+0.005; +0.008] |
| a caldo, 1 epoca a giro − da zero, 1 epoca | +0.005 [+0.002; +0.008] | sì | [+0.002; +0.008] |
| da zero, 1 epoca − mai aggiornare | +0.046 [+0.040; +0.052] | sì | [+0.041; +0.051] |
| e-means di Faiss 1.16.0, impostazioni di serie + liste ricostruite − mai aggiornare | -0.358 [-0.370; -0.345] | sì | [-0.371; -0.339] |
| e-means di Faiss 1.16.0, impostazioni di serie − e-means: massa no, rianimazione sì, medie finali sì | +0.002 [+0.000; +0.003] | sì | [-0.000; +0.003] |

Scomposizione dell'uso ingenuo: e-means sui soli testi nuovi, dai centroidi vecchi. Recall con l'1% letto.

| Massa iniziale | Rianimazione | Medie finali | Dopo 1 giro | Dopo 10 giri | Dopo 10 giri, liste ricostruite |
|---|---|---|---|---|---|
| no | sì | sì | 0.115 [0.108; 0.123] | 0.048 [0.044; 0.051] | 0.379 [0.370; 0.389] |
| no | sì | no | 0.096 [0.089; 0.103] | 0.045 [0.042; 0.049] | 0.392 [0.381; 0.402] |
| no | no | sì | 0.188 [0.179; 0.198] | 0.104 [0.099; 0.109] | 0.148 [0.143; 0.155] |
| no | no | no | 0.186 [0.176; 0.196] | 0.103 [0.098; 0.108] | 0.137 [0.132; 0.143] |
| sì | sì | sì | 0.619 [0.608; 0.631] | 0.365 [0.356; 0.376] | 0.508 [0.499; 0.519] |
| sì | sì | no | 0.792 [0.782; 0.802] | 0.773 [0.766; 0.781] | 0.786 [0.779; 0.794] |
| sì | no | sì | 0.619 [0.608; 0.631] | 0.365 [0.355; 0.376] | 0.504 [0.494; 0.514] |
| sì | no | no | 0.792 [0.782; 0.801] | 0.773 [0.765; 0.781] | 0.783 [0.776; 0.791] |

Per confronto, dopo 10 giri: mai aggiornare 0.746; riferimento 0.821.

Addestramento dei centroidi sui 200.000 testi, implementazioni di Faiss (mediana di 6 ripetizioni; la riassegnazione dei vettori non è compresa nel tempo):

| Metodo | Passate | Tempo | Errore di addestramento | Errore sui testi tenuti fuori | Recall, 1% letto |
|---|---|---|---|---|---|
| e-means | 1 | 2.3 s | 0.4196 | 0.4293 | 0.791 |
| e-means | 2 | 4.5 s | 0.4101 | 0.4226 | 0.811 |
| e-means | 3 | 6.7 s | 0.4079 | 0.4204 | 0.815 |
| e-means | 5 | 10.9 s | 0.4066 | 0.4196 | 0.819 |
| e-means | 10 | 21.8 s | 0.4057 | 0.4191 | 0.820 |
| k-means | 3 | 3.6 s | 0.4177 | 0.4288 | 0.807 |
| k-means | 5 | 5.9 s | 0.4134 | 0.4253 | 0.815 |
| k-means | 10 | 11.8 s | 0.4101 | 0.4227 | 0.820 |
| k-means | 12 | 14.3 s | 0.4096 | 0.4224 | 0.821 |
| k-means | 15 | 17.8 s | 0.4092 | 0.4220 | 0.821 |
| k-means | 20 | 23.7 s | 0.4088 | 0.4217 | 0.821 |
| k-means | 25 | 29.7 s | 0.4086 | 0.4215 | 0.821 |

A parità di errore di addestramento: il k-means non raggiunge e-means a 3 epoche nemmeno con 25 iterazioni (29.7 s contro 6.7 s): rapporto dei tempi superiore a 4.4.

A parità di errore sui testi tenuti fuori: il k-means non raggiunge e-means a 3 epoche nemmeno con 25 iterazioni (29.7 s contro 6.7 s): rapporto dei tempi superiore a 4.4.

A parità di recall con lo 0,1% dell'indice letto: il k-means non raggiunge e-means a 3 epoche nemmeno con 25 iterazioni (29.7 s contro 6.7 s): rapporto dei tempi superiore a 4.4.

A parità di recall con l'1% dell'indice letto: al k-means servono tra 3 e 5 iterazioni, cioè tra 3.6 e 5.9 s contro 6.7 s di e-means a 3 epoche: rapporto dei tempi tra 0.5 e 0.9.

## abstract arXiv, bge-base-en-v1.5 (768 dimensioni)

Risultati mancanti.
