## Data: separated

Rules fitted on the overlapping data, datasets 0, 1, 2:

- constant: log m = -1.61 -0.00 · log(signal) -0.00 · log(f)
- from the signal: log m = -2.07 -0.45 · log(signal) +0.00 · log(f)
- from the share: log m = -1.84 +0.00 · log(signal) -0.30 · log(f)
- from the signal and the share: log m = -2.42 -0.50 · log(signal) -0.40 · log(f)

Evaluation on datasets 5, 6, 7. Error on all data relative to mini-batch k-means with true counts, median: negative = better. The oracle is the best mass of the grid chosen by looking at the result.

| Share of new points | Drift | Signal | oracle m | m from the signal | Old centroids | Oracle | constant | from the signal | from the share | from the signal and the share |
|---|---|---|---|---|---|---|---|---|---|---|
| 5% | none | +0.013 | 1 | 0.88 | +0.03% | +0.00% | +0.15% | +0.00% | +0.03% | +0.01% |
| 5% | a quarter of the new points shifted | +1.291 | 0.5 | 0.11 | +0.56% | -0.03% | +0.59% | +1.97% | -0.00% | +0.20% |
| 5% | half of the new points shifted | +2.278 | 0.5 | 0.09 | +1.92% | -0.60% | -0.18% | +2.31% | -0.51% | -0.12% |
| 5% | all shifted slightly | +3.811 | 0.5 | 0.07 | +3.22% | -0.29% | +0.97% | +9.04% | -0.20% | +2.51% |
| 5% | all shifted | +4.991 | 0.5 | 0.06 | +5.88% | -0.23% | +1.03% | +8.93% | -0.03% | +2.82% |
| 20% | none | +0.012 | 1 | 0.91 | +0.11% | +0.01% | +0.34% | +0.01% | +0.23% | +0.02% |
| 20% | a quarter of the new points shifted | +1.222 | 0.5 | 0.12 | +6.05% | -0.34% | +0.39% | +1.46% | +0.12% | +0.92% |
| 20% | half of the new points shifted | +2.444 | 0.01 | 0.08 | +15.61% | -4.05% | -0.98% | -1.05% | -0.96% | -0.78% |
| 20% | all shifted slightly | +3.836 | 0.2 | 0.07 | +27.15% | -1.73% | -0.61% | -1.01% | -0.25% | -1.70% |
| 20% | all shifted | +4.969 | 0.02 | 0.06 | +31.02% | -4.33% | -2.28% | -4.46% | -2.29% | -4.67% |
| 50% | none | +0.013 | 2 | 0.88 | +0.26% | +0.02% | +0.18% | +0.03% | +0.18% | +0.02% |
| 50% | a quarter of the new points shifted | +1.195 | 0.01 | 0.12 | +20.80% | -9.56% | -2.14% | -2.98% | -2.15% | -3.64% |
| 50% | half of the new points shifted | +2.499 | 0.01 | 0.08 | +45.21% | -23.36% | -8.82% | -13.59% | -8.92% | -13.50% |
| 50% | all shifted slightly | +3.847 | 0.1 | 0.07 | +95.81% | -16.69% | -13.75% | -15.68% | -13.70% | -15.55% |
| 50% | all shifted | +4.981 | 0.02 | 0.06 | +92.21% | -28.00% | -15.33% | -24.08% | -14.70% | -24.13% |

| Summary over the 15 cases | Mean | Worst case | Cases worse than mini-batch by more than 0.05 points |
|---|---|---|---|
| oracle | -5.94% | +0.02% | 0 |
| constant | -2.70% | +1.03% | 7 |
| from the signal | -2.60% | +9.04% | 5 |
| from the share | -2.88% | +0.23% | 3 |
| from the signal and the share | -3.84% | +2.82% | 4 |
