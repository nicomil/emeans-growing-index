Corpus: arxiv.
Indice iniziale: 100000 articoli, dal 2007-04-01 al 2016-08-01.
10 giri da 10000 articoli, fino al 2021-09-01. 2048 liste, 3 seed dell'algoritmo, un solo corpus.
Recall@10 leggendo l'1% dell'indice. Mediana su 3 seed; [min; max] è la sola variabilità dell'algoritmo.
Gli articoli dopo il 2021-09-01 restano fuori dall'esperimento.


### Dopo 1 giro (indice fino al 2017-04-01; 1534 interrogazioni, di cui 145 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall | [min; max] | Recall, periodo iniziale | Recall, periodo aggiunto |
|---|---|---|---|---|---|
| mai aggiornare | +0.73% | 0.931 | [0.931; 0.932] | 0.932 | 0.930 |
| e-means, impostazioni di serie (solo nuovi) | +137.38% | 0.228 | [0.228; 0.239] | 0.224 | 0.270 |
| mini-batch dalle dimensioni delle liste (solo nuovi) | +0.51% | 0.932 | [0.930; 0.932] | 0.932 | 0.931 |
| e-means, massa 0,2 (solo nuovi) | +1.38% | 0.931 | [0.927; 0.931] | 0.931 | 0.923 |
| a caldo su tutti i dati, 1 epoca | +4.02% | 0.920 | [0.916; 0.922] | 0.920 | 0.914 |
| a caldo su tutti i dati, 3 epoche | +0.60% | 0.931 | [0.930; 0.931] | 0.932 | 0.921 |
| da zero su tutti i dati, 1 epoca | +4.46% | 0.917 | [0.915; 0.920] | 0.917 | 0.921 |
| da zero su tutti i dati, 3 epoche | +0.87% | 0.931 | [0.929; 0.933] | 0.932 | 0.930 |
| da zero su tutti i dati, 10 epoche (riferimento) | +0.00% | 0.934 | [0.933; 0.934] | 0.934 | 0.923 |

### Dopo 5 giri (indice fino al 2019-07-01; 2145 interrogazioni, di cui 756 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall | [min; max] | Recall, periodo iniziale | Recall, periodo aggiunto |
|---|---|---|---|---|---|
| mai aggiornare | +2.31% | 0.929 | [0.928; 0.929] | 0.935 | 0.917 |
| e-means, impostazioni di serie (solo nuovi) | +197.71% | 0.086 | [0.085; 0.088] | 0.072 | 0.112 |
| mini-batch dalle dimensioni delle liste (solo nuovi) | +1.27% | 0.932 | [0.932; 0.932] | 0.936 | 0.925 |
| e-means, massa 0,2 (solo nuovi) | +3.22% | 0.928 | [0.926; 0.929] | 0.931 | 0.923 |
| a caldo su tutti i dati, 1 epoca | +3.08% | 0.926 | [0.926; 0.927] | 0.927 | 0.925 |
| a caldo su tutti i dati, 3 epoche | +0.53% | 0.937 | [0.935; 0.937] | 0.938 | 0.935 |
| da zero su tutti i dati, 1 epoca | +3.80% | 0.923 | [0.922; 0.926] | 0.925 | 0.922 |
| da zero su tutti i dati, 3 epoche | +0.68% | 0.936 | [0.934; 0.938] | 0.936 | 0.935 |
| da zero su tutti i dati, 10 epoche (riferimento) | +0.00% | 0.939 | [0.938; 0.940] | 0.939 | 0.938 |

### Dopo 10 giri (indice fino al 2021-09-01; 2900 interrogazioni, di cui 1511 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall | [min; max] | Recall, periodo iniziale | Recall, periodo aggiunto |
|---|---|---|---|---|---|
| mai aggiornare | +4.25% | 0.919 | [0.915; 0.920] | 0.937 | 0.901 |
| e-means, impostazioni di serie (solo nuovi) | +198.61% | 0.070 | [0.070; 0.072] | 0.052 | 0.087 |
| mini-batch dalle dimensioni delle liste (solo nuovi) | +2.16% | 0.930 | [0.929; 0.931] | 0.940 | 0.921 |
| e-means, massa 0,2 (solo nuovi) | +4.24% | 0.928 | [0.927; 0.928] | 0.934 | 0.921 |
| a caldo su tutti i dati, 1 epoca | +2.46% | 0.934 | [0.933; 0.936] | 0.934 | 0.934 |
| a caldo su tutti i dati, 3 epoche | +0.30% | 0.943 | [0.942; 0.944] | 0.942 | 0.942 |
| da zero su tutti i dati, 1 epoca | +3.05% | 0.934 | [0.934; 0.935] | 0.934 | 0.934 |
| da zero su tutti i dati, 3 epoche | +0.47% | 0.943 | [0.943; 0.944] | 0.943 | 0.943 |
| da zero su tutti i dati, 10 epoche (riferimento) | +0.00% | 0.946 | [0.944; 0.947] | 0.945 | 0.946 |
| mai aggiornare, articoli in ordine casuale (controllo senza deriva) | +2.04% | 0.940 | [0.937; 0.940] | 0.940 | 0.939 |

### Ricalcolo completo sull'indice finale, implementazioni di Faiss (8 thread)

Una misura per seed, nell'ordine della tabella, nello stesso processo. Errore sui dati di addestramento.

| Metodo | Tempo mediano | Errore mediano |
|---|---|---|
| e-means di Faiss, 3 epoche | 4.4 s | 0.5053 |
| k-means di Faiss, 3 iterazioni | 2.8 s | 0.5180 |
| k-means di Faiss, 5 iterazioni | 4.6 s | 0.5125 |
| k-means di Faiss, 10 iterazioni | 9.1 s | 0.5083 |
| k-means di Faiss, 25 iterazioni | 22.8 s | 0.5061 |
