Indice iniziale: 100000 articoli, dal 2012-01-28 al 2015-02-08.
10 giri da 10000 articoli, fino al 2019-09-01. 2048 liste, 3 seed dell'algoritmo, un solo corpus.
Recall@10 leggendo l'1% dell'indice. Mediana su 3 seed; [min; max] è la sola variabilità dell'algoritmo.
Gli articoli dopo il 2019-09-01 restano fuori dall'esperimento.


### Dopo 1 giro (indice fino al 2015-06-06; 1536 interrogazioni, di cui 146 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall | [min; max] | Recall, periodo iniziale | Recall, periodo aggiunto |
|---|---|---|---|---|---|
| mai aggiornare | +0.76% | 0.829 | [0.824; 0.830] | 0.830 | 0.805 |
| e-means, impostazioni di serie (solo nuovi) | +117.65% | 0.153 | [0.150; 0.154] | 0.142 | 0.247 |
| mini-batch dalle dimensioni delle liste (solo nuovi) | +0.53% | 0.827 | [0.824; 0.830] | 0.828 | 0.808 |
| e-means, massa 0,2 (solo nuovi) | +1.28% | 0.824 | [0.821; 0.828] | 0.826 | 0.805 |
| a caldo su tutti i dati, 1 epoca | +4.14% | 0.798 | [0.795; 0.800] | 0.801 | 0.771 |
| a caldo su tutti i dati, 3 epoche | +0.60% | 0.826 | [0.824; 0.826] | 0.827 | 0.803 |
| da zero su tutti i dati, 1 epoca | +4.98% | 0.797 | [0.792; 0.800] | 0.799 | 0.780 |
| da zero su tutti i dati, 3 epoche | +0.94% | 0.825 | [0.824; 0.826] | 0.827 | 0.806 |
| da zero su tutti i dati, 10 epoche (riferimento) | +0.00% | 0.834 | [0.831; 0.835] | 0.836 | 0.815 |

### Dopo 5 giri (indice fino al 2016-09-10; 2136 interrogazioni, di cui 746 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall | [min; max] | Recall, periodo iniziale | Recall, periodo aggiunto |
|---|---|---|---|---|---|
| mai aggiornare | +3.19% | 0.806 | [0.804; 0.810] | 0.835 | 0.757 |
| e-means, impostazioni di serie (solo nuovi) | +146.55% | 0.072 | [0.068; 0.077] | 0.038 | 0.135 |
| mini-batch dalle dimensioni delle liste (solo nuovi) | +1.73% | 0.817 | [0.813; 0.819] | 0.837 | 0.781 |
| e-means, massa 0,2 (solo nuovi) | +3.47% | 0.818 | [0.817; 0.820] | 0.833 | 0.788 |
| a caldo su tutti i dati, 1 epoca | +3.25% | 0.812 | [0.809; 0.814] | 0.820 | 0.796 |
| a caldo su tutti i dati, 3 epoche | +0.53% | 0.834 | [0.832; 0.834] | 0.839 | 0.823 |
| da zero su tutti i dati, 1 epoca | +4.15% | 0.809 | [0.808; 0.810] | 0.816 | 0.801 |
| da zero su tutti i dati, 3 epoche | +0.80% | 0.833 | [0.832; 0.836] | 0.840 | 0.819 |
| da zero su tutti i dati, 10 epoche (riferimento) | +0.00% | 0.840 | [0.838; 0.840] | 0.844 | 0.831 |

### Dopo 10 giri (indice fino al 2019-09-01; 2898 interrogazioni, di cui 1508 del periodo aggiunto)

| Strategia | Errore nelle liste | Recall | [min; max] | Recall, periodo iniziale | Recall, periodo aggiunto |
|---|---|---|---|---|---|
| mai aggiornare | +5.61% | 0.781 | [0.779; 0.783] | 0.839 | 0.728 |
| e-means, impostazioni di serie (solo nuovi) | +143.66% | 0.052 | [0.052; 0.054] | 0.023 | 0.080 |
| mini-batch dalle dimensioni delle liste (solo nuovi) | +2.84% | 0.805 | [0.801; 0.806] | 0.847 | 0.765 |
| e-means, massa 0,2 (solo nuovi) | +4.87% | 0.808 | [0.805; 0.808] | 0.841 | 0.776 |
| a caldo su tutti i dati, 1 epoca | +2.64% | 0.824 | [0.821; 0.825] | 0.837 | 0.811 |
| a caldo su tutti i dati, 3 epoche | +0.34% | 0.840 | [0.837; 0.840] | 0.851 | 0.829 |
| da zero su tutti i dati, 1 epoca | +3.33% | 0.822 | [0.819; 0.822] | 0.833 | 0.810 |
| da zero su tutti i dati, 3 epoche | +0.58% | 0.838 | [0.837; 0.842] | 0.849 | 0.828 |
| da zero su tutti i dati, 10 epoche (riferimento) | +0.00% | 0.843 | [0.842; 0.843] | 0.851 | 0.835 |
| mai aggiornare, articoli in ordine casuale (controllo senza deriva) | +1.99% | 0.831 | [0.828; 0.832] | 0.838 | 0.823 |

### Ricalcolo completo sull'indice finale, implementazioni di Faiss (8 thread)

Una misura per seed, nell'ordine della tabella, nello stesso processo. Errore sui dati di addestramento.

| Metodo | Tempo mediano | Errore mediano |
|---|---|---|
| e-means di Faiss, 3 epoche | 4.4 s | 0.6099 |
| k-means di Faiss, 3 iterazioni | 2.8 s | 0.6264 |
| k-means di Faiss, 5 iterazioni | 4.6 s | 0.6192 |
| k-means di Faiss, 10 iterazioni | 9.2 s | 0.6136 |
| k-means di Faiss, 25 iterazioni | 22.7 s | 0.6108 |
