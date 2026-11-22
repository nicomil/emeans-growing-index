## Dati netti

Regole tarate sui dati sovrapposti, insiemi di dati 0, 1, 2:

- costante: log m = -1.61 -0.00 · log(segnale) -0.00 · log(f)
- dal segnale: log m = -2.07 -0.45 · log(segnale) +0.00 · log(f)
- dalla quota: log m = -1.84 +0.00 · log(segnale) -0.30 · log(f)
- dal segnale e dalla quota: log m = -2.42 -0.50 · log(segnale) -0.40 · log(f)

Valutazione sugli insiemi di dati 5, 6, 7. Errore su tutti i dati rispetto al mini-batch k-means con conteggi veri, mediana: negativo = meglio. L'oracolo è la migliore massa della griglia scelta guardando il risultato.

| Quota nuovi | Deriva | Segnale | m oracolo | m dal segnale | Centroidi vecchi | Oracolo | costante | dal segnale | dalla quota | dal segnale e dalla quota |
|---|---|---|---|---|---|---|---|---|---|---|
| 5% | nessuna | +0.013 | 1 | 0.88 | +0.03% | +0.00% | +0.15% | +0.00% | +0.03% | +0.01% |
| 5% | un quarto dei nuovi spostati | +1.291 | 0.5 | 0.11 | +0.56% | -0.03% | +0.59% | +1.97% | -0.00% | +0.20% |
| 5% | metà dei nuovi spostati | +2.278 | 0.5 | 0.09 | +1.92% | -0.60% | -0.18% | +2.31% | -0.51% | -0.12% |
| 5% | tutti spostati di poco | +3.811 | 0.5 | 0.07 | +3.22% | -0.29% | +0.97% | +9.04% | -0.20% | +2.51% |
| 5% | tutti spostati | +4.991 | 0.5 | 0.06 | +5.88% | -0.23% | +1.03% | +8.93% | -0.03% | +2.82% |
| 20% | nessuna | +0.012 | 1 | 0.91 | +0.11% | +0.01% | +0.34% | +0.01% | +0.23% | +0.02% |
| 20% | un quarto dei nuovi spostati | +1.222 | 0.5 | 0.12 | +6.05% | -0.34% | +0.39% | +1.46% | +0.12% | +0.92% |
| 20% | metà dei nuovi spostati | +2.444 | 0.01 | 0.08 | +15.61% | -4.05% | -0.98% | -1.05% | -0.96% | -0.78% |
| 20% | tutti spostati di poco | +3.836 | 0.2 | 0.07 | +27.15% | -1.73% | -0.61% | -1.01% | -0.25% | -1.70% |
| 20% | tutti spostati | +4.969 | 0.02 | 0.06 | +31.02% | -4.33% | -2.28% | -4.46% | -2.29% | -4.67% |
| 50% | nessuna | +0.013 | 2 | 0.88 | +0.26% | +0.02% | +0.18% | +0.03% | +0.18% | +0.02% |
| 50% | un quarto dei nuovi spostati | +1.195 | 0.01 | 0.12 | +20.80% | -9.56% | -2.14% | -2.98% | -2.15% | -3.64% |
| 50% | metà dei nuovi spostati | +2.499 | 0.01 | 0.08 | +45.21% | -23.36% | -8.82% | -13.59% | -8.92% | -13.50% |
| 50% | tutti spostati di poco | +3.847 | 0.1 | 0.07 | +95.81% | -16.69% | -13.75% | -15.68% | -13.70% | -15.55% |
| 50% | tutti spostati | +4.981 | 0.02 | 0.06 | +92.21% | -28.00% | -15.33% | -24.08% | -14.70% | -24.13% |

| Riepilogo sui 15 casi | Media | Caso peggiore | Casi peggiori del mini-batch di oltre 0.05 punti |
|---|---|---|---|
| oracolo | -5.94% | +0.02% | 0 |
| costante | -2.70% | +1.03% | 7 |
| dal segnale | -2.60% | +9.04% | 5 |
| dalla quota | -2.88% | +0.23% | 3 |
| dal segnale e dalla quota | -3.84% | +2.82% | 4 |
