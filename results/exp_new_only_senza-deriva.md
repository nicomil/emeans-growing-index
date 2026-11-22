## Dati senza-deriva

5 insiemi di dati × 2 seed dell'algoritmo. Le 10 esecuzioni non sono indipendenti: centroidi vecchi e strategie senza casualità cambiano solo con l'insieme di dati.

Errore in eccesso rispetto al riferimento della stessa esecuzione: mediana [minimo; massimo].

### 5% di punti nuovi (2631 punti, batch 64, passo della legge 0.078)

| Strategia | Letture | Tutti i dati | Solo punti vecchi | Solo punti nuovi |
|---|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | 0.00 × n | +0.14% [+0.12; +0.16] | +0.06% | +1.83% |
| e-means, massa quasi nulla e finalizzazione | 0.05 × n | +17.86% [+17.45; +18.26] | +18.90% | -2.31% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.05 × n | +0.11% [+0.09; +0.13] | +0.08% | +0.85% |
| mini-batch k-means con conteggi veri | 0.05 × n | +0.11% [+0.09; +0.13] | +0.08% | +0.84% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.05 × n | +0.16% [+0.13; +0.17] | +0.18% | -0.35% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.15 × n | +0.11% [+0.09; +0.13] | +0.08% | +0.84% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.15 × n | +0.78% [+0.76; +0.80] | +1.04% | -4.36% |
| a caldo su tutti i dati, 1 epoca | tutti i dati | +0.84% [+0.73; +0.99] | +0.84% | +0.94% |
| da zero su tutti i dati, 1 epoca | tutti i dati | +3.17% [+2.94; +3.52] | +3.18% | +3.14% |

Griglia di e-means, una passata sui punti nuovi, senza finalizzazione. Eccesso mediano su tutti i dati; tra parentesi in quante esecuzioni su 10 batte il mini-batch k-means con conteggi veri.

Rianimazione con soglia 0.1:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +2.31% (0) | +2.39% (0) | +2.78% (0) | +5.17% (0) |
| 0.1 | +0.47% (0) | +0.49% (0) | +0.60% (0) | +1.70% (0) |
| 0.3 | +0.14% (0) | +0.14% (0) | +0.16% (0) | +0.39% (0) |
| 1 | +0.12% (0) | +0.12% (0) | +0.12% (0) | +0.12% (0) |
| 3 | +0.13% (0) | +0.13% (0) | +0.13% (0) | +0.12% (0) |

Rianimazione spenta:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +2.31% (0) | +2.39% (0) | +2.78% (0) | +5.17% (0) |
| 0.1 | +0.47% (0) | +0.49% (0) | +0.60% (0) | +1.70% (0) |
| 0.3 | +0.14% (0) | +0.14% (0) | +0.16% (0) | +0.39% (0) |
| 1 | +0.12% (0) | +0.12% (0) | +0.12% (0) | +0.12% (0) |
| 3 | +0.13% (0) | +0.13% (0) | +0.13% (0) | +0.12% (0) |

### 20% di punti nuovi (12500 punti, batch 256, passo della legge 0.135)

| Strategia | Letture | Tutti i dati | Solo punti vecchi | Solo punti nuovi |
|---|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | 0.00 × n | +0.28% [+0.25; +0.31] | -0.08% | +1.71% |
| e-means, massa quasi nulla e finalizzazione | 0.20 × n | +7.54% [+7.07; +7.91] | +8.62% | +3.19% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.20 × n | +0.16% [+0.13; +0.19] | -0.00% | +0.82% |
| mini-batch k-means con conteggi veri | 0.20 × n | +0.16% [+0.13; +0.19] | +0.01% | +0.77% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.20 × n | +0.29% [+0.26; +0.32] | +0.41% | -0.22% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.60 × n | +0.16% [+0.13; +0.19] | +0.01% | +0.76% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.60 × n | +1.06% [+1.00; +1.09] | +1.74% | -1.71% |
| a caldo su tutti i dati, 1 epoca | tutti i dati | +0.80% [+0.69; +0.85] | +0.79% | +0.80% |
| da zero su tutti i dati, 1 epoca | tutti i dati | +2.85% [+2.55; +3.09] | +2.85% | +2.85% |

Griglia di e-means, una passata sui punti nuovi, senza finalizzazione. Eccesso mediano su tutti i dati; tra parentesi in quante esecuzioni su 10 batte il mini-batch k-means con conteggi veri.

Rianimazione con soglia 0.1:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +1.73% (0) | +1.75% (0) | +1.85% (0) | +2.85% (0) |
| 0.1 | +0.65% (0) | +0.68% (0) | +0.86% (0) | +2.22% (0) |
| 0.3 | +0.22% (0) | +0.23% (0) | +0.29% (0) | +1.52% (0) |
| 1 | +0.19% (0) | +0.19% (0) | +0.17% (0) | +0.68% (0) |
| 3 | +0.24% (0) | +0.24% (0) | +0.22% (0) | +0.24% (0) |

Rianimazione spenta:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +1.73% (0) | +1.75% (0) | +1.85% (0) | +2.85% (0) |
| 0.1 | +0.65% (0) | +0.68% (0) | +0.86% (0) | +2.22% (0) |
| 0.3 | +0.22% (0) | +0.23% (0) | +0.29% (0) | +1.52% (0) |
| 1 | +0.19% (0) | +0.19% (0) | +0.17% (0) | +0.68% (0) |
| 3 | +0.24% (0) | +0.24% (0) | +0.22% (0) | +0.24% (0) |

### 50% di punti nuovi (50000 punti, batch 1024, passo della legge 0.252)

| Strategia | Letture | Tutti i dati | Solo punti vecchi | Solo punti nuovi |
|---|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | 0.00 × n | +0.49% [+0.46; +0.52] | -0.39% | +1.35% |
| e-means, massa quasi nulla e finalizzazione | 0.50 × n | +1.08% [+0.95; +1.28] | +1.75% | +0.40% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.50 × n | +0.19% [+0.17; +0.22] | -0.20% | +0.59% |
| mini-batch k-means con conteggi veri | 0.50 × n | +0.17% [+0.15; +0.20] | -0.16% | +0.50% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.50 × n | +0.27% [+0.25; +0.29] | +0.46% | +0.07% |
| Lloyd sui nuovi con statistiche vecchie congelate | 1.50 × n | +0.16% [+0.14; +0.18] | -0.15% | +0.46% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 1.50 × n | +0.37% [+0.35; +0.38] | +0.98% | -0.26% |
| a caldo su tutti i dati, 1 epoca | tutti i dati | +0.33% [+0.32; +0.34] | +0.32% | +0.35% |
| da zero su tutti i dati, 1 epoca | tutti i dati | +1.84% [+1.58; +2.14] | +1.88% | +1.84% |

Griglia di e-means, una passata sui punti nuovi, senza finalizzazione. Eccesso mediano su tutti i dati; tra parentesi in quante esecuzioni su 10 batte il mini-batch k-means con conteggi veri.

Rianimazione con soglia 0.1:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +0.68% (0) | +0.66% (0) | +0.59% (0) | +0.84% (0) |
| 0.1 | +0.40% (0) | +0.40% (0) | +0.42% (0) | +0.82% (0) |
| 0.3 | +0.22% (0) | +0.22% (0) | +0.27% (0) | +0.79% (0) |
| 1 | +0.23% (0) | +0.22% (0) | +0.17% (0) | +0.75% (0) |
| 3 | +0.35% (0) | +0.33% (0) | +0.24% (0) | +0.69% (0) |

Rianimazione spenta:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +0.68% (0) | +0.66% (0) | +0.59% (0) | +0.85% (0) |
| 0.1 | +0.40% (0) | +0.40% (0) | +0.42% (0) | +0.82% (0) |
| 0.3 | +0.22% (0) | +0.22% (0) | +0.27% (0) | +0.79% (0) |
| 1 | +0.23% (0) | +0.22% (0) | +0.17% (0) | +0.75% (0) |
| 3 | +0.35% (0) | +0.33% (0) | +0.24% (0) | +0.69% (0) |
