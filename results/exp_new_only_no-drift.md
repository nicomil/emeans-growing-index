## Data: no-drift

5 datasets × 2 algorithm seeds. The 10 runs are not independent: old centroids and strategies without randomness change only with the dataset.

Excess error relative to the reference of the same run: median [minimum; maximum].

### 5% new points (2631 points, batch 64, step of the law 0.078)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +0.14% [+0.12; +0.16] | +0.06% | +1.83% |
| e-means, near-zero mass and finalization | 0.05 × n | +17.86% [+17.45; +18.26] | +18.90% | -2.31% |
| Lloyd on the new points with frozen old statistics | 0.05 × n | +0.11% [+0.09; +0.13] | +0.08% | +0.85% |
| mini-batch k-means with true counts | 0.05 × n | +0.11% [+0.09; +0.13] | +0.08% | +0.84% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.05 × n | +0.16% [+0.13; +0.17] | +0.18% | -0.35% |
| Lloyd on the new points with frozen old statistics | 0.15 × n | +0.11% [+0.09; +0.13] | +0.08% | +0.84% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.15 × n | +0.78% [+0.76; +0.80] | +1.04% | -4.36% |
| warm start on all data, 1 epoch | all data | +0.84% [+0.73; +0.99] | +0.84% | +0.94% |
| from scratch on all data, 1 epoch | all data | +3.17% [+2.94; +3.52] | +3.18% | +3.14% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +2.31% (0) | +2.39% (0) | +2.78% (0) | +5.17% (0) |
| 0.1 | +0.47% (0) | +0.49% (0) | +0.60% (0) | +1.70% (0) |
| 0.3 | +0.14% (0) | +0.14% (0) | +0.16% (0) | +0.39% (0) |
| 1 | +0.12% (0) | +0.12% (0) | +0.12% (0) | +0.12% (0) |
| 3 | +0.13% (0) | +0.13% (0) | +0.13% (0) | +0.12% (0) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +2.31% (0) | +2.39% (0) | +2.78% (0) | +5.17% (0) |
| 0.1 | +0.47% (0) | +0.49% (0) | +0.60% (0) | +1.70% (0) |
| 0.3 | +0.14% (0) | +0.14% (0) | +0.16% (0) | +0.39% (0) |
| 1 | +0.12% (0) | +0.12% (0) | +0.12% (0) | +0.12% (0) |
| 3 | +0.13% (0) | +0.13% (0) | +0.13% (0) | +0.12% (0) |

### 20% new points (12500 points, batch 256, step of the law 0.135)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +0.28% [+0.25; +0.31] | -0.08% | +1.71% |
| e-means, near-zero mass and finalization | 0.20 × n | +7.54% [+7.07; +7.91] | +8.62% | +3.19% |
| Lloyd on the new points with frozen old statistics | 0.20 × n | +0.16% [+0.13; +0.19] | -0.00% | +0.82% |
| mini-batch k-means with true counts | 0.20 × n | +0.16% [+0.13; +0.19] | +0.01% | +0.77% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.20 × n | +0.29% [+0.26; +0.32] | +0.41% | -0.22% |
| Lloyd on the new points with frozen old statistics | 0.60 × n | +0.16% [+0.13; +0.19] | +0.01% | +0.76% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.60 × n | +1.06% [+1.00; +1.09] | +1.74% | -1.71% |
| warm start on all data, 1 epoch | all data | +0.80% [+0.69; +0.85] | +0.79% | +0.80% |
| from scratch on all data, 1 epoch | all data | +2.85% [+2.55; +3.09] | +2.85% | +2.85% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +1.73% (0) | +1.75% (0) | +1.85% (0) | +2.85% (0) |
| 0.1 | +0.65% (0) | +0.68% (0) | +0.86% (0) | +2.22% (0) |
| 0.3 | +0.22% (0) | +0.23% (0) | +0.29% (0) | +1.52% (0) |
| 1 | +0.19% (0) | +0.19% (0) | +0.17% (0) | +0.68% (0) |
| 3 | +0.24% (0) | +0.24% (0) | +0.22% (0) | +0.24% (0) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +1.73% (0) | +1.75% (0) | +1.85% (0) | +2.85% (0) |
| 0.1 | +0.65% (0) | +0.68% (0) | +0.86% (0) | +2.22% (0) |
| 0.3 | +0.22% (0) | +0.23% (0) | +0.29% (0) | +1.52% (0) |
| 1 | +0.19% (0) | +0.19% (0) | +0.17% (0) | +0.68% (0) |
| 3 | +0.24% (0) | +0.24% (0) | +0.22% (0) | +0.24% (0) |

### 50% new points (50000 points, batch 1024, step of the law 0.252)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +0.49% [+0.46; +0.52] | -0.39% | +1.35% |
| e-means, near-zero mass and finalization | 0.50 × n | +1.08% [+0.95; +1.28] | +1.75% | +0.40% |
| Lloyd on the new points with frozen old statistics | 0.50 × n | +0.19% [+0.17; +0.22] | -0.20% | +0.59% |
| mini-batch k-means with true counts | 0.50 × n | +0.17% [+0.15; +0.20] | -0.16% | +0.50% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.50 × n | +0.27% [+0.25; +0.29] | +0.46% | +0.07% |
| Lloyd on the new points with frozen old statistics | 1.50 × n | +0.16% [+0.14; +0.18] | -0.15% | +0.46% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 1.50 × n | +0.37% [+0.35; +0.38] | +0.98% | -0.26% |
| warm start on all data, 1 epoch | all data | +0.33% [+0.32; +0.34] | +0.32% | +0.35% |
| from scratch on all data, 1 epoch | all data | +1.84% [+1.58; +2.14] | +1.88% | +1.84% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +0.68% (0) | +0.66% (0) | +0.59% (0) | +0.84% (0) |
| 0.1 | +0.40% (0) | +0.40% (0) | +0.42% (0) | +0.82% (0) |
| 0.3 | +0.22% (0) | +0.22% (0) | +0.27% (0) | +0.79% (0) |
| 1 | +0.23% (0) | +0.22% (0) | +0.17% (0) | +0.75% (0) |
| 3 | +0.35% (0) | +0.33% (0) | +0.24% (0) | +0.69% (0) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +0.68% (0) | +0.66% (0) | +0.59% (0) | +0.85% (0) |
| 0.1 | +0.40% (0) | +0.40% (0) | +0.42% (0) | +0.82% (0) |
| 0.3 | +0.22% (0) | +0.22% (0) | +0.27% (0) | +0.79% (0) |
| 1 | +0.23% (0) | +0.22% (0) | +0.17% (0) | +0.75% (0) |
| 3 | +0.35% (0) | +0.33% (0) | +0.24% (0) | +0.69% (0) |
