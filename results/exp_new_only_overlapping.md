## Data: overlapping

5 datasets × 2 algorithm seeds. The 10 runs are not independent: old centroids and strategies without randomness change only with the dataset.

Excess error relative to the reference of the same run: median [minimum; maximum].

### 5% new points (2631 points, batch 64, step of the law 0.078)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +2.35% [+2.15; +2.50] | -0.30% | +44.57% |
| e-means, near-zero mass and finalization | 0.05 × n | +66.40% [+63.48; +68.35] | +72.23% | -24.37% |
| Lloyd on the new points with frozen old statistics | 0.05 × n | +1.69% [+1.48; +1.90] | -0.05% | +29.45% |
| mini-batch k-means with true counts | 0.05 × n | +1.29% [+1.14; +1.45] | -0.12% | +24.31% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.05 × n | +1.27% [+1.07; +1.37] | +0.15% | +19.23% |
| Lloyd on the new points with frozen old statistics | 0.15 × n | +1.27% [+1.08; +1.42] | -0.08% | +23.00% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.15 × n | +1.65% [+1.36; +1.91] | +1.26% | +7.33% |
| warm start on all data, 1 epoch | all data | +1.36% [+1.22; +1.64] | +0.84% | +9.97% |
| from scratch on all data, 1 epoch | all data | +3.85% [+3.56; +4.24] | +3.62% | +8.21% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +2.67% (0) | +2.73% (0) | +2.94% (0) | +4.39% (0) |
| 0.1 | +1.48% (0) | +1.50% (0) | +1.59% (0) | +2.29% (0) |
| 0.3 | +1.27% (9) | +1.27% (10) | +1.27% (9) | +1.39% (1) |
| 1 | +1.43% (0) | +1.42% (0) | +1.35% (0) | +1.24% (10) |
| 3 | +2.02% (0) | +2.01% (0) | +1.91% (0) | +1.45% (0) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +2.67% (0) | +2.73% (0) | +2.94% (0) | +4.39% (0) |
| 0.1 | +1.48% (0) | +1.50% (0) | +1.59% (0) | +2.29% (0) |
| 0.3 | +1.27% (9) | +1.27% (10) | +1.27% (9) | +1.39% (1) |
| 1 | +1.43% (0) | +1.42% (0) | +1.35% (0) | +1.24% (10) |
| 3 | +2.02% (0) | +2.01% (0) | +1.91% (0) | +1.45% (0) |

### 20% new points (12500 points, batch 256, step of the law 0.135)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +12.65% [+12.06; +12.84] | -0.95% | +66.09% |
| e-means, near-zero mass and finalization | 0.20 × n | +54.78% [+51.79; +58.12] | +70.71% | -8.08% |
| Lloyd on the new points with frozen old statistics | 0.20 × n | +7.09% [+6.77; +7.54] | +0.61% | +32.75% |
| mini-batch k-means with true counts | 0.20 × n | +6.37% [+5.70; +6.56] | -0.26% | +32.15% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.20 × n | +4.89% [+4.41; +5.37] | +0.92% | +20.70% |
| Lloyd on the new points with frozen old statistics | 0.60 × n | +5.46% [+5.26; +5.84] | +0.16% | +26.56% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.60 × n | +4.41% [+3.54; +5.09] | +4.57% | +3.72% |
| warm start on all data, 1 epoch | all data | +1.98% [+1.71; +2.27] | +1.34% | +4.68% |
| from scratch on all data, 1 epoch | all data | +3.60% [+3.27; +4.04] | +4.25% | +1.04% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +5.50% (10) | +5.74% (10) | +7.02% (0) | +48.09% (0) |
| 0.1 | +4.54% (10) | +4.53% (10) | +4.23% (10) | +31.70% (0) |
| 0.3 | +5.46% (10) | +5.33% (10) | +4.89% (10) | +5.16% (10) |
| 1 | +7.03% (0) | +6.93% (0) | +6.45% (0) | +4.37% (10) |
| 3 | +8.02% (0) | +7.92% (0) | +7.63% (0) | +5.22% (10) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +5.21% (10) | +5.26% (10) | +5.52% (10) | +10.99% (0) |
| 0.1 | +4.54% (10) | +4.53% (10) | +4.23% (10) | +6.80% (0) |
| 0.3 | +5.46% (10) | +5.33% (10) | +4.89% (10) | +4.60% (10) |
| 1 | +7.03% (0) | +6.93% (0) | +6.45% (0) | +4.37% (10) |
| 3 | +8.02% (0) | +7.92% (0) | +7.63% (0) | +5.22% (10) |

### 50% new points (50000 points, batch 1024, step of the law 0.252)

| Strategy | Reads | All data | Old points only | New points only |
|---|---|---|---|---|
| old centroids, no recomputation | 0.00 × n | +31.48% [+29.81; +32.71] | -5.89% | +71.85% |
| e-means, near-zero mass and finalization | 0.50 × n | +31.54% [+29.25; +33.20] | +63.13% | -2.82% |
| Lloyd on the new points with frozen old statistics | 0.50 × n | +12.62% [+11.79; +13.55] | -1.48% | +27.67% |
| mini-batch k-means with true counts | 0.50 × n | +9.01% [+7.85; +10.16] | -3.84% | +22.39% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 0.50 × n | +3.25% [+2.53; +4.53] | -1.27% | +8.42% |
| Lloyd on the new points with frozen old statistics | 1.50 × n | +6.32% [+5.08; +7.10] | -2.23% | +15.39% |
| e-means, fixed configuration (m 0.3; s 1/4; no revival) | 1.50 × n | +7.27% [+6.03; +8.21] | +13.22% | +0.82% |
| warm start on all data, 1 epoch | all data | +0.25% [-0.15; +0.74] | -2.39% | +3.15% |
| from scratch on all data, 1 epoch | all data | +2.13% [+1.94; +2.62] | +3.34% | +0.90% |

Grid of e-means, one pass over the new points, without finalization. Median excess on all data; in parentheses, in how many runs out of 10 it beats mini-batch k-means with true counts.

Revival with threshold 0.1:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +17.72% (0) | +18.46% (0) | +22.80% (0) | +30.35% (0) |
| 0.1 | +3.35% (10) | +3.44% (10) | +13.55% (0) | +29.88% (0) |
| 0.3 | +5.91% (10) | +5.29% (10) | +3.44% (10) | +29.47% (0) |
| 1 | +11.13% (0) | +10.37% (0) | +7.05% (10) | +27.39% (0) |
| 3 | +15.85% (0) | +15.25% (0) | +12.04% (0) | +24.08% (0) |

Revival off:

| mass m | step ×1/64 | step ×1/16 | step ×1/4 | step ×1/1 |
|---|---|---|---|---|
| 0.03 | +4.00% (10) | +4.14% (10) | +5.70% (10) | +15.66% (0) |
| 0.1 | +3.17% (10) | +2.97% (10) | +2.77% (10) | +13.77% (0) |
| 0.3 | +5.91% (10) | +5.29% (10) | +3.25% (10) | +11.56% (0) |
| 1 | +11.13% (0) | +10.37% (0) | +7.05% (10) | +8.40% (8) |
| 3 | +15.85% (0) | +15.25% (0) | +12.04% (0) | +5.37% (10) |
