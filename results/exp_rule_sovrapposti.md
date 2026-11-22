## Dati sovrapposti

Regole tarate sui dati sovrapposti, insiemi di dati 0, 1, 2:

- costante: log m = -1.61 -0.00 · log(segnale) -0.00 · log(f)
- dal segnale: log m = -2.07 -0.45 · log(segnale) +0.00 · log(f)
- dalla quota: log m = -1.84 +0.00 · log(segnale) -0.30 · log(f)
- dal segnale e dalla quota: log m = -2.42 -0.50 · log(segnale) -0.40 · log(f)

Valutazione sugli insiemi di dati 5, 6, 7. Errore su tutti i dati rispetto al mini-batch k-means con conteggi veri, mediana: negativo = meglio. L'oracolo è la migliore massa della griglia scelta guardando il risultato.

| Quota nuovi | Deriva | Segnale | m oracolo | m dal segnale | Centroidi vecchi | Oracolo | costante | dal segnale | dalla quota | dal segnale e dalla quota |
|---|---|---|---|---|---|---|---|---|---|---|
| 5% | nessuna | +0.016 | 1 | 0.81 | +0.03% | +0.01% | +0.12% | +0.00% | +0.02% | +0.02% |
| 5% | un quarto dei nuovi spostati | +0.178 | 0.5 | 0.27 | +0.10% | -0.02% | +0.05% | +0.00% | -0.02% | +0.00% |
| 5% | metà dei nuovi spostati | +0.310 | 0.5 | 0.21 | +0.27% | -0.02% | +0.06% | +0.04% | -0.04% | -0.02% |
| 5% | tutti spostati di poco | +0.337 | 0.5 | 0.21 | +0.16% | -0.01% | +0.13% | +0.11% | -0.01% | -0.01% |
| 5% | tutti spostati | +0.687 | 0.5 | 0.15 | +1.03% | -0.03% | +0.03% | +0.11% | -0.04% | -0.04% |
| 20% | nessuna | +0.017 | 1 | 0.79 | +0.12% | +0.01% | +0.29% | +0.01% | +0.18% | +0.02% |
| 20% | un quarto dei nuovi spostati | +0.174 | 0.5 | 0.28 | +1.10% | -0.05% | +0.14% | +0.01% | +0.03% | -0.08% |
| 20% | metà dei nuovi spostati | +0.357 | 0.2 | 0.20 | +2.78% | -0.20% | -0.20% | -0.20% | -0.23% | -0.23% |
| 20% | tutti spostati di poco | +0.356 | 0.2 | 0.20 | +2.08% | -0.81% | -0.81% | -0.81% | -0.82% | -0.75% |
| 20% | tutti spostati | +0.705 | 0.1 | 0.15 | +5.99% | -2.01% | -1.67% | -1.82% | -1.42% | -1.58% |
| 50% | nessuna | +0.018 | 1 | 0.77 | +0.31% | +0.00% | +0.15% | +0.01% | +0.15% | +0.00% |
| 50% | un quarto dei nuovi spostati | +0.185 | 0.02 | 0.27 | +3.72% | -1.35% | -0.78% | -0.68% | -0.76% | -0.64% |
| 50% | metà dei nuovi spostati | +0.356 | 0.02 | 0.20 | +8.46% | -3.90% | -2.81% | -2.83% | -2.77% | -2.81% |
| 50% | tutti spostati di poco | +0.357 | 0.5 | 0.20 | +10.76% | -2.16% | -2.00% | -2.00% | -1.96% | -2.00% |
| 50% | tutti spostati | +0.707 | 0.2 | 0.15 | +20.66% | -5.53% | -5.60% | -5.72% | -5.42% | -5.66% |

| Riepilogo sui 15 casi | Media | Caso peggiore | Casi peggiori del mini-batch di oltre 0.05 punti |
|---|---|---|---|
| oracolo | -1.07% | +0.01% | 0 |
| costante | -0.86% | +0.29% | 7 |
| dal segnale | -0.92% | +0.11% | 2 |
| dalla quota | -0.87% | +0.18% | 2 |
| dal segnale e dalla quota | -0.92% | +0.02% | 0 |
