## Dati sovrapposti

5 insiemi di dati × 2 seed dell'algoritmo. Le 10 esecuzioni non sono indipendenti: centroidi vecchi e strategie senza casualità cambiano solo con l'insieme di dati.

Errore in eccesso rispetto al riferimento della stessa esecuzione: mediana [minimo; massimo].

### 5% di punti nuovi (2631 punti, batch 64, passo della legge 0.078)

| Strategia | Letture | Tutti i dati | Solo punti vecchi | Solo punti nuovi |
|---|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | 0.00 × n | +2.35% [+2.15; +2.50] | -0.30% | +44.57% |
| e-means, massa quasi nulla e finalizzazione | 0.05 × n | +66.40% [+63.48; +68.35] | +72.23% | -24.37% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.05 × n | +1.69% [+1.48; +1.90] | -0.05% | +29.45% |
| mini-batch k-means con conteggi veri | 0.05 × n | +1.29% [+1.14; +1.45] | -0.12% | +24.31% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.05 × n | +1.27% [+1.07; +1.37] | +0.15% | +19.23% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.15 × n | +1.27% [+1.08; +1.42] | -0.08% | +23.00% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.15 × n | +1.65% [+1.36; +1.91] | +1.26% | +7.33% |
| a caldo su tutti i dati, 1 epoca | tutti i dati | +1.36% [+1.22; +1.64] | +0.84% | +9.97% |
| da zero su tutti i dati, 1 epoca | tutti i dati | +3.85% [+3.56; +4.24] | +3.62% | +8.21% |

Griglia di e-means, una passata sui punti nuovi, senza finalizzazione. Eccesso mediano su tutti i dati; tra parentesi in quante esecuzioni su 10 batte il mini-batch k-means con conteggi veri.

Rianimazione con soglia 0.1:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +2.67% (0) | +2.73% (0) | +2.94% (0) | +4.39% (0) |
| 0.1 | +1.48% (0) | +1.50% (0) | +1.59% (0) | +2.29% (0) |
| 0.3 | +1.27% (9) | +1.27% (10) | +1.27% (9) | +1.39% (1) |
| 1 | +1.43% (0) | +1.42% (0) | +1.35% (0) | +1.24% (10) |
| 3 | +2.02% (0) | +2.01% (0) | +1.91% (0) | +1.45% (0) |

Rianimazione spenta:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +2.67% (0) | +2.73% (0) | +2.94% (0) | +4.39% (0) |
| 0.1 | +1.48% (0) | +1.50% (0) | +1.59% (0) | +2.29% (0) |
| 0.3 | +1.27% (9) | +1.27% (10) | +1.27% (9) | +1.39% (1) |
| 1 | +1.43% (0) | +1.42% (0) | +1.35% (0) | +1.24% (10) |
| 3 | +2.02% (0) | +2.01% (0) | +1.91% (0) | +1.45% (0) |

### 20% di punti nuovi (12500 punti, batch 256, passo della legge 0.135)

| Strategia | Letture | Tutti i dati | Solo punti vecchi | Solo punti nuovi |
|---|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | 0.00 × n | +12.65% [+12.06; +12.84] | -0.95% | +66.09% |
| e-means, massa quasi nulla e finalizzazione | 0.20 × n | +54.78% [+51.79; +58.12] | +70.71% | -8.08% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.20 × n | +7.09% [+6.77; +7.54] | +0.61% | +32.75% |
| mini-batch k-means con conteggi veri | 0.20 × n | +6.37% [+5.70; +6.56] | -0.26% | +32.15% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.20 × n | +4.89% [+4.41; +5.37] | +0.92% | +20.70% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.60 × n | +5.46% [+5.26; +5.84] | +0.16% | +26.56% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.60 × n | +4.41% [+3.54; +5.09] | +4.57% | +3.72% |
| a caldo su tutti i dati, 1 epoca | tutti i dati | +1.98% [+1.71; +2.27] | +1.34% | +4.68% |
| da zero su tutti i dati, 1 epoca | tutti i dati | +3.60% [+3.27; +4.04] | +4.25% | +1.04% |

Griglia di e-means, una passata sui punti nuovi, senza finalizzazione. Eccesso mediano su tutti i dati; tra parentesi in quante esecuzioni su 10 batte il mini-batch k-means con conteggi veri.

Rianimazione con soglia 0.1:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +5.50% (10) | +5.74% (10) | +7.02% (0) | +48.09% (0) |
| 0.1 | +4.54% (10) | +4.53% (10) | +4.23% (10) | +31.70% (0) |
| 0.3 | +5.46% (10) | +5.33% (10) | +4.89% (10) | +5.16% (10) |
| 1 | +7.03% (0) | +6.93% (0) | +6.45% (0) | +4.37% (10) |
| 3 | +8.02% (0) | +7.92% (0) | +7.63% (0) | +5.22% (10) |

Rianimazione spenta:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +5.21% (10) | +5.26% (10) | +5.52% (10) | +10.99% (0) |
| 0.1 | +4.54% (10) | +4.53% (10) | +4.23% (10) | +6.80% (0) |
| 0.3 | +5.46% (10) | +5.33% (10) | +4.89% (10) | +4.60% (10) |
| 1 | +7.03% (0) | +6.93% (0) | +6.45% (0) | +4.37% (10) |
| 3 | +8.02% (0) | +7.92% (0) | +7.63% (0) | +5.22% (10) |

### 50% di punti nuovi (50000 punti, batch 1024, passo della legge 0.252)

| Strategia | Letture | Tutti i dati | Solo punti vecchi | Solo punti nuovi |
|---|---|---|---|---|
| centroidi vecchi, nessun ricalcolo | 0.00 × n | +31.48% [+29.81; +32.71] | -5.89% | +71.85% |
| e-means, massa quasi nulla e finalizzazione | 0.50 × n | +31.54% [+29.25; +33.20] | +63.13% | -2.82% |
| Lloyd sui nuovi con statistiche vecchie congelate | 0.50 × n | +12.62% [+11.79; +13.55] | -1.48% | +27.67% |
| mini-batch k-means con conteggi veri | 0.50 × n | +9.01% [+7.85; +10.16] | -3.84% | +22.39% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 0.50 × n | +3.25% [+2.53; +4.53] | -1.27% | +8.42% |
| Lloyd sui nuovi con statistiche vecchie congelate | 1.50 × n | +6.32% [+5.08; +7.10] | -2.23% | +15.39% |
| e-means, configurazione fissa (m 0,3; s 1/4; senza rianimazione) | 1.50 × n | +7.27% [+6.03; +8.21] | +13.22% | +0.82% |
| a caldo su tutti i dati, 1 epoca | tutti i dati | +0.25% [-0.15; +0.74] | -2.39% | +3.15% |
| da zero su tutti i dati, 1 epoca | tutti i dati | +2.13% [+1.94; +2.62] | +3.34% | +0.90% |

Griglia di e-means, una passata sui punti nuovi, senza finalizzazione. Eccesso mediano su tutti i dati; tra parentesi in quante esecuzioni su 10 batte il mini-batch k-means con conteggi veri.

Rianimazione con soglia 0.1:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +17.72% (0) | +18.46% (0) | +22.80% (0) | +30.35% (0) |
| 0.1 | +3.35% (10) | +3.44% (10) | +13.55% (0) | +29.88% (0) |
| 0.3 | +5.91% (10) | +5.29% (10) | +3.44% (10) | +29.47% (0) |
| 1 | +11.13% (0) | +10.37% (0) | +7.05% (10) | +27.39% (0) |
| 3 | +15.85% (0) | +15.25% (0) | +12.04% (0) | +24.08% (0) |

Rianimazione spenta:

| massa m | passo ×1/64 | passo ×1/16 | passo ×1/4 | passo ×1/1 |
|---|---|---|---|---|
| 0.03 | +4.00% (10) | +4.14% (10) | +5.70% (10) | +15.66% (0) |
| 0.1 | +3.17% (10) | +2.97% (10) | +2.77% (10) | +13.77% (0) |
| 0.3 | +5.91% (10) | +5.29% (10) | +3.25% (10) | +11.56% (0) |
| 1 | +11.13% (0) | +10.37% (0) | +7.05% (10) | +8.40% (8) |
| 3 | +15.85% (0) | +15.25% (0) | +12.04% (0) | +5.37% (10) |
