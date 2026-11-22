10 giri da 2500 punti nuovi su 50000 iniziali; 5 insiemi di dati.

Errore in eccesso rispetto a e-means da zero su tutti i dati, 10 epoche, rifatto a ogni giro. Mediana; dove indicato anche [minimo; massimo]. Il riferimento vede i punti nuovi mentre si addestra: una parte dell'eccesso dei centroidi mai aggiornati è questo, non degrado.
Letture in 10 giri: 25000 punti per le strategie sui soli nuovi, 637500 per quella che rilegge tutto.

### Deriva: nessuna

| Strategia | Liste, dopo 1 giro | dopo 5 | dopo 10 | Liste, colpo unico | Riassegnando, dopo 10 | Riassegnando, colpo unico | Punti iniziali nelle loro liste, dopo 10 |
|---|---|---|---|---|---|---|---|
| centroidi iniziali, mai aggiornati | +0.12% | +0.27% | +0.36% [+0.35; +0.42] | +0.36% | +0.36% [+0.35; +0.42] | +0.36% | +0.00% |
| e-means, massa quasi nulla e finalizzazione | +78.20% | +127.52% | +130.09% [+128.04; +133.27] | +22.15% | +18.77% [+18.28; +19.09] | +3.49% | +137.25% |
| mini-batch k-means dalle dimensioni delle liste | +0.09% | +0.17% | +0.18% [+0.17; +0.24] | +0.18% | +0.15% [+0.14; +0.22] | +0.15% | +0.19% |
| e-means, massa 1 | +0.10% | +0.18% | +0.20% [+0.19; +0.27] | +0.20% | +0.19% [+0.18; +0.25] | +0.16% | +0.12% |
| e-means, massa dalla quota | +0.12% | +0.26% | +0.30% [+0.29; +0.36] | +0.69% | +0.20% [+0.19; +0.26] | +0.38% | +0.54% |
| e-means, massa 0,2 | +0.27% | +0.71% | +0.86% [+0.85; +0.93] | +0.75% | +0.48% [+0.45; +0.53] | +0.42% | +1.55% |
| a caldo su tutti i dati, 1 epoca | +0.80% | +0.79% | +0.59% [+0.51; +0.63] | +0.64% | +0.59% [+0.51; +0.63] | +0.64% | +0.78% |

### Deriva: zona nuova fissa

| Strategia | Liste, dopo 1 giro | dopo 5 | dopo 10 | Liste, colpo unico | Riassegnando, dopo 10 | Riassegnando, colpo unico | Punti iniziali nelle loro liste, dopo 10 |
|---|---|---|---|---|---|---|---|
| centroidi iniziali, mai aggiornati | +2.02% | +11.56% | +19.73% [+18.52; +22.53] | +19.73% | +19.73% [+18.52; +22.53] | +19.73% | +0.00% |
| e-means, massa quasi nulla e finalizzazione | +165.72% | +169.57% | +166.32% [+157.53; +168.17] | +96.76% | +45.36% [+44.09; +49.87] | +41.91% | +199.91% |
| mini-batch k-means dalle dimensioni delle liste | +1.24% | +6.50% | +9.78% [+9.39; +11.70] | +8.75% | +8.08% [+7.77; +9.84] | +7.99% | +2.32% |
| e-means, massa 1 | +1.27% | +6.78% | +10.30% [+9.90; +12.33] | +8.54% | +9.39% [+8.95; +11.25] | +7.64% | +1.52% |
| e-means, massa dalla quota | +1.33% | +6.41% | +9.29% [+8.98; +11.12] | +8.42% | +5.99% [+5.51; +7.21] | +4.86% | +4.91% |
| e-means, massa 0,2 | +1.69% | +7.60% | +10.43% [+9.72; +11.55] | +8.50% | +3.38% [+3.30; +4.31] | +4.54% | +9.64% |
| a caldo su tutti i dati, 1 epoca | +1.21% | +1.52% | +0.97% [+0.84; +1.23] | +1.53% | +0.97% [+0.84; +1.23] | +1.53% | +3.01% |

### Deriva: zona che si allontana

| Strategia | Liste, dopo 1 giro | dopo 5 | dopo 10 | Liste, colpo unico | Riassegnando, dopo 10 | Riassegnando, colpo unico | Punti iniziali nelle loro liste, dopo 10 |
|---|---|---|---|---|---|---|---|
| centroidi iniziali, mai aggiornati | +0.53% | +4.32% | +10.48% [+9.95; +12.18] | +10.48% | +10.48% [+9.95; +12.18] | +10.48% | +0.00% |
| e-means, massa quasi nulla e finalizzazione | +101.30% | +141.15% | +169.87% [+164.46; +176.95] | +63.73% | +49.00% [+48.29; +53.10] | +18.12% | +198.28% |
| mini-batch k-means dalle dimensioni delle liste | +0.47% | +3.45% | +6.33% [+5.99; +7.50] | +6.02% | +5.23% [+4.63; +6.06] | +5.51% | +2.28% |
| e-means, massa 1 | +0.48% | +3.60% | +6.76% [+6.57; +8.00] | +5.92% | +6.20% [+5.77; +7.27] | +5.29% | +1.37% |
| e-means, massa dalla quota | +0.52% | +3.67% | +6.47% [+6.13; +7.70] | +6.88% | +3.58% [+2.94; +3.97] | +3.81% | +5.39% |
| e-means, massa 0,2 | +0.80% | +5.57% | +9.55% [+9.12; +10.81] | +7.15% | +2.72% [+2.38; +2.84] | +3.86% | +12.74% |
| a caldo su tutti i dati, 1 epoca | +1.27% | +1.29% | +1.30% [+1.17; +1.63] | +1.86% | +1.30% [+1.17; +1.63] | +1.86% | +3.00% |
