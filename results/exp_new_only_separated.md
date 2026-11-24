## Data: separated

5 datasets × 2 algorithm seeds. The 10 runs are not independent: old centroids and strategies without randomness change only with the dataset.

Excess error relative to the reference of the same run: median [minimum; maximum].

### 5% new points (2631 points, batch 64, step of the law 0.078)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +12.24% [+9.14; +19.31] | -5.40% | +184.43% |
| e-means, near-zero mass and finalization | 0.05 × n | +438.51% [+421.89; +482.87] | +486.69% | -61.28% |
| Lloyd on the new points with frozen old statistics | 0.05 × n | +7.63% [+4.64; +14.13] | -3.26% | +116.65% |
| mini-batch k-means with true counts | 0.05 × n | +5.95% [+1.97; +11.58] | -3.11% | +96.25% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.05 × n | +5.84% [+0.75; +11.26] | -0.36% | +65.80% |
| Lloyd on the new points with frozen old statistics | 0.15 × n | +5.49% [+1.59; +10.92] | -2.43% | +88.12% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.15 × n | +9.98% [+1.91; +15.92] | +9.34% | +23.00% |
| warm start on all data, 1 epoch | all data | -1.95% [-4.99; +4.50] | -6.34% | +43.14% |
| from scratch on all data, 1 epoch | all data | +4.11% [+1.19; +8.47] | +3.40% | +8.51% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +17.44% (0) | +17.55% (0) | +17.86% (0) | +19.62% (0) |
| 0.1 | +8.61% (1) | +8.87% (1) | +9.50% (0) | +11.86% (0) |
| 0.3 | +5.69% (10) | +5.75% (9) | +5.84% (9) | +8.07% (1) |
| 1 | +6.98% (0) | +6.88% (0) | +6.55% (0) | +5.62% (9) |
| 3 | +9.70% (0) | +9.57% (0) | +9.05% (0) | +7.05% (0) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +17.44% (0) | +17.55% (0) | +17.86% (0) | +19.56% (0) |
| 0.1 | +8.61% (1) | +8.87% (1) | +9.50% (0) | +11.86% (0) |
| 0.3 | +5.69% (10) | +5.75% (9) | +5.84% (9) | +8.07% (1) |
| 1 | +6.98% (0) | +6.88% (0) | +6.55% (0) | +5.62% (9) |
| 3 | +9.70% (0) | +9.57% (0) | +9.05% (0) | +7.05% (0) |

### 20% new points (12500 points, batch 256, step of the law 0.135)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +79.84% [+69.42; +86.35] | -11.28% | +479.75% |
| e-means, near-zero mass and finalization | 0.20 × n | +370.66% [+349.14; +406.60] | +455.27% | -15.92% |
| Lloyd on the new points with frozen old statistics | 0.20 × n | +39.71% [+33.61; +44.61] | -0.89% | +211.10% |
| mini-batch k-means with true counts | 0.20 × n | +31.64% [+25.04; +36.75] | -4.13% | +189.48% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.20 × n | +26.71% [+20.36; +32.60] | +5.02% | +125.23% |
| Lloyd on the new points with frozen old statistics | 0.60 × n | +24.45% [+12.93; +29.83] | +2.69% | +112.46% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.60 × n | +23.79% [+15.21; +31.30] | +9.55% | +81.99% |
| warm start on all data, 1 epoch | all data | +5.20% [-1.11; +9.55] | -5.85% | +46.87% |
| from scratch on all data, 1 epoch | all data | +6.47% [-3.19; +11.07] | +5.97% | +6.70% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +29.17% (6) | +33.39% (4) | +100.22% (0) | +382.34% (0) |
| 0.1 | +24.72% (10) | +24.73% (10) | +24.30% (10) | +308.72% (0) |
| 0.3 | +28.44% (10) | +27.38% (10) | +26.71% (10) | +44.89% (0) |
| 1 | +35.66% (0) | +34.85% (0) | +31.97% (2) | +27.11% (10) |
| 3 | +47.79% (0) | +46.69% (0) | +41.96% (0) | +28.46% (10) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +24.43% (10) | +24.64% (10) | +24.49% (10) | +25.35% (10) |
| 0.1 | +24.72% (10) | +24.73% (10) | +24.09% (10) | +23.06% (10) |
| 0.3 | +28.44% (10) | +27.38% (10) | +26.71% (10) | +25.41% (10) |
| 1 | +35.66% (0) | +34.85% (0) | +31.97% (2) | +27.10% (10) |
| 3 | +47.79% (0) | +46.69% (0) | +41.96% (0) | +28.46% (10) |

### 50% new points (50000 points, batch 1024, step of the law 0.252)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +168.21% [+144.85; +184.20] | -41.55% | +556.86% |
| e-means, near-zero mass and finalization | 0.50 × n | +177.36% [+154.63; +198.58] | +275.04% | -2.56% |
| Lloyd on the new points with frozen old statistics | 0.50 × n | +41.49% [+26.21; +53.32] | -18.89% | +166.94% |
| mini-batch k-means with true counts | 0.50 × n | +31.15% [+19.15; +46.92] | -30.22% | +148.88% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.50 × n | +13.63% [-1.31; +24.35] | -25.37% | +91.86% |
| Lloyd on the new points with frozen old statistics | 1.50 × n | -1.12% [-14.91; +11.18] | -20.95% | +33.61% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 1.50 × n | +4.34% [-8.43; +12.20] | -20.06% | +46.35% |
| warm start on all data, 1 epoch | all data | -20.37% [-28.36; -13.41] | -33.71% | +4.83% |
| from scratch on all data, 1 epoch | all data | -2.23% [-6.36; +2.01] | -3.99% | +1.06% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +137.80% (0) | +150.53% (0) | +178.17% (0) | +181.81% (0) |
| 0.1 | +12.37% (10) | +28.04% (7) | +128.59% (0) | +182.20% (0) |
| 0.3 | +15.37% (10) | +14.72% (10) | +7.35% (10) | +182.28% (0) |
| 1 | +34.94% (0) | +33.33% (0) | +28.14% (10) | +180.71% (0) |
| 3 | +57.87% (0) | +54.75% (0) | +42.19% (0) | +181.06% (0) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | -1.09% (10) | -1.34% (10) | -0.93% (10) | -0.68% (10) |
| 0.1 | +5.58% (10) | +5.39% (10) | +4.34% (10) | -0.52% (10) |
| 0.3 | +15.37% (10) | +14.92% (10) | +13.63% (10) | +8.97% (10) |
| 1 | +34.94% (0) | +33.33% (0) | +28.14% (10) | +16.43% (10) |
| 3 | +57.87% (0) | +54.75% (0) | +42.19% (0) | +20.21% (10) |
