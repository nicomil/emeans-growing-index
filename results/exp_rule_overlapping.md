## Data: overlapping

Rules fitted on the overlapping data, datasets 0, 1, 2:

- constant: log m = -1.61 -0.00 · log(signal) -0.00 · log(f)
- from the signal: log m = -2.07 -0.45 · log(signal) +0.00 · log(f)
- from the share: log m = -1.84 +0.00 · log(signal) -0.30 · log(f)
- from the signal and the share: log m = -2.42 -0.50 · log(signal) -0.40 · log(f)

Evaluation on datasets 5, 6, 7. Error on all data relative to mini-batch k-means with true counts, median: negative = better. The oracle is the best mass of the grid chosen by looking at the result.

| Share of new points | Drift | Signal | oracle m | m from the signal | Old centroids | Oracle | constant | from the signal | from the share | from the signal and the share |
|---|---|---|---|---|---|---|---|---|---|---|
| 5% | none | +0.016 | 1 | 0.81 | +0.03% | +0.01% | +0.12% | +0.00% | +0.02% | +0.02% |
| 5% | a quarter of the new points shifted | +0.178 | 0.5 | 0.27 | +0.10% | -0.02% | +0.05% | +0.00% | -0.02% | +0.00% |
| 5% | half of the new points shifted | +0.310 | 0.5 | 0.21 | +0.27% | -0.02% | +0.06% | +0.04% | -0.04% | -0.02% |
| 5% | all shifted slightly | +0.337 | 0.5 | 0.21 | +0.16% | -0.01% | +0.13% | +0.11% | -0.01% | -0.01% |
| 5% | all shifted | +0.687 | 0.5 | 0.15 | +1.03% | -0.03% | +0.03% | +0.11% | -0.04% | -0.04% |
| 20% | none | +0.017 | 1 | 0.79 | +0.12% | +0.01% | +0.29% | +0.01% | +0.18% | +0.02% |
| 20% | a quarter of the new points shifted | +0.174 | 0.5 | 0.28 | +1.10% | -0.05% | +0.14% | +0.01% | +0.03% | -0.08% |
| 20% | half of the new points shifted | +0.357 | 0.2 | 0.20 | +2.78% | -0.20% | -0.20% | -0.20% | -0.23% | -0.23% |
| 20% | all shifted slightly | +0.356 | 0.2 | 0.20 | +2.08% | -0.81% | -0.81% | -0.81% | -0.82% | -0.75% |
| 20% | all shifted | +0.705 | 0.1 | 0.15 | +5.99% | -2.01% | -1.67% | -1.82% | -1.42% | -1.58% |
| 50% | none | +0.018 | 1 | 0.77 | +0.31% | +0.00% | +0.15% | +0.01% | +0.15% | +0.00% |
| 50% | a quarter of the new points shifted | +0.185 | 0.02 | 0.27 | +3.72% | -1.35% | -0.78% | -0.68% | -0.76% | -0.64% |
| 50% | half of the new points shifted | +0.356 | 0.02 | 0.20 | +8.46% | -3.90% | -2.81% | -2.83% | -2.77% | -2.81% |
| 50% | all shifted slightly | +0.357 | 0.5 | 0.20 | +10.76% | -2.16% | -2.00% | -2.00% | -1.96% | -2.00% |
| 50% | all shifted | +0.707 | 0.2 | 0.15 | +20.66% | -5.53% | -5.60% | -5.72% | -5.42% | -5.66% |

| Summary over the 15 cases | Mean | Worst case | Cases worse than mini-batch by more than 0.05 points |
|---|---|---|---|
| oracle | -1.07% | +0.01% | 0 |
| constant | -0.86% | +0.29% | 7 |
| from the signal | -0.92% | +0.11% | 2 |
| from the share | -0.87% | +0.18% | 2 |
| from the signal and the share | -0.92% | +0.02% | 0 |
