Dataset: arxiv, 384 dimensions.
Initial index: 100000 texts, from 2007-04-01 to 2016-08-01.
10 rounds of 10000 texts, up to 2021-09-01. 2048 lists, 3 algorithm seeds.
Recall@10 reading 0.1% and 1% of the index. Median over 3 seeds. The intervals are in results/SUMMARY.md.


### After 1 round (index up to 2017-04-01; 1534 queries, of which 145 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +0.73% | 0.558 | 0.931 | 0.929 |
| Faiss 1.16.0 e-means, default settings | +135.05% | 0.084 | 0.230 | 0.292 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +25.84% | 0.169 | 0.652 | 0.676 |
| e-means: mass no, revival yes, final means yes | +137.38% | 0.083 | 0.229 | 0.269 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +25.88% | 0.173 | 0.660 | 0.685 |
| e-means: mass no, revival yes, final means no | +149.56% | 0.056 | 0.181 | 0.221 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +26.75% | 0.192 | 0.673 | 0.685 |
| e-means: mass no, revival no, final means yes | +88.82% | 0.136 | 0.391 | 0.392 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +24.10% | 0.167 | 0.677 | 0.702 |
| e-means: mass no, revival no, final means no | +89.20% | 0.134 | 0.392 | 0.399 |
| e-means: mass no, revival no, final means no + lists rebuilt | +24.94% | 0.167 | 0.666 | 0.690 |
| e-means: mass yes, revival yes, final means yes | +25.83% | 0.447 | 0.836 | 0.839 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +15.75% | 0.439 | 0.883 | 0.878 |
| e-means: mass yes, revival yes, final means no | +0.54% | 0.560 | 0.932 | 0.929 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +0.53% | 0.561 | 0.933 | 0.928 |
| e-means: mass yes, revival no, final means yes | +25.83% | 0.447 | 0.836 | 0.839 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +15.75% | 0.439 | 0.883 | 0.878 |
| e-means: mass yes, revival no, final means no | +0.54% | 0.560 | 0.932 | 0.929 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +0.53% | 0.561 | 0.933 | 0.928 |
| mini-batch k-means from the list sizes | +0.51% | 0.560 | 0.932 | 0.930 |
| mini-batch k-means from the list sizes + lists rebuilt | +0.50% | 0.561 | 0.932 | 0.930 |
| e-means: mass 0.2, step/4, no revival, no final means | +1.38% | 0.555 | 0.931 | 0.922 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +1.24% | 0.556 | 0.931 | 0.923 |
| warm start, 1 epoch per round | +4.02% | 0.506 | 0.920 | 0.914 |
| warm start, 3 epochs per round | +0.60% | 0.554 | 0.931 | 0.923 |
| warm start with steady-state mass, 3 epochs per round | +0.24% | 0.562 | 0.933 | 0.926 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.37% | 0.560 | 0.932 | 0.928 |
| from scratch, 1 epoch | +4.46% | 0.501 | 0.918 | 0.920 |
| from scratch, 3 epochs | +0.87% | 0.551 | 0.931 | 0.929 |
| from scratch, 10 epochs (reference) | +0.00% | 0.565 | 0.934 | 0.926 |

### After 5 rounds (index up to 2019-07-01; 2145 queries, of which 756 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +2.31% | 0.549 | 0.929 | 0.917 |
| Faiss 1.16.0 e-means, default settings | +197.40% | 0.041 | 0.088 | 0.115 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +23.16% | 0.224 | 0.743 | 0.750 |
| e-means: mass no, revival yes, final means yes | +197.71% | 0.042 | 0.086 | 0.112 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +23.30% | 0.215 | 0.738 | 0.746 |
| e-means: mass no, revival yes, final means no | +186.65% | 0.032 | 0.077 | 0.098 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +24.33% | 0.223 | 0.719 | 0.727 |
| e-means: mass no, revival no, final means yes | +109.41% | 0.060 | 0.246 | 0.284 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +29.90% | 0.091 | 0.484 | 0.509 |
| e-means: mass no, revival no, final means no | +109.46% | 0.058 | 0.249 | 0.292 |
| e-means: mass no, revival no, final means no + lists rebuilt | +31.01% | 0.090 | 0.468 | 0.489 |
| e-means: mass yes, revival yes, final means yes | +53.27% | 0.287 | 0.619 | 0.652 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +17.77% | 0.288 | 0.827 | 0.833 |
| e-means: mass yes, revival yes, final means no | +1.38% | 0.555 | 0.932 | 0.926 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +1.25% | 0.558 | 0.933 | 0.928 |
| e-means: mass yes, revival no, final means yes | +53.27% | 0.287 | 0.618 | 0.653 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +17.77% | 0.287 | 0.827 | 0.833 |
| e-means: mass yes, revival no, final means no | +1.36% | 0.555 | 0.932 | 0.926 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +1.25% | 0.558 | 0.933 | 0.928 |
| mini-batch k-means from the list sizes | +1.27% | 0.555 | 0.932 | 0.925 |
| mini-batch k-means from the list sizes + lists rebuilt | +1.20% | 0.560 | 0.933 | 0.927 |
| e-means: mass 0.2, step/4, no revival, no final means | +3.22% | 0.546 | 0.928 | 0.924 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +2.45% | 0.556 | 0.933 | 0.931 |
| warm start, 1 epoch per round | +3.08% | 0.534 | 0.927 | 0.926 |
| warm start, 3 epochs per round | +0.53% | 0.578 | 0.936 | 0.934 |
| warm start with steady-state mass, 3 epochs per round | +0.20% | 0.585 | 0.937 | 0.936 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.30% | 0.583 | 0.937 | 0.935 |
| from scratch, 1 epoch | +3.80% | 0.525 | 0.923 | 0.922 |
| from scratch, 3 epochs | +0.68% | 0.578 | 0.937 | 0.936 |
| from scratch, 10 epochs (reference) | +0.00% | 0.584 | 0.939 | 0.938 |

### After 10 rounds (index up to 2021-09-01; 2900 queries, of which 1511 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +4.25% | 0.536 | 0.919 | 0.901 |
| Faiss 1.16.0 e-means, default settings | +200.53% | 0.032 | 0.069 | 0.086 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +23.24% | 0.232 | 0.741 | 0.757 |
| e-means: mass no, revival yes, final means yes | +198.61% | 0.033 | 0.071 | 0.087 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +23.11% | 0.238 | 0.755 | 0.766 |
| e-means: mass no, revival yes, final means no | +190.77% | 0.026 | 0.062 | 0.075 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +23.70% | 0.241 | 0.732 | 0.747 |
| e-means: mass no, revival no, final means yes | +119.20% | 0.047 | 0.226 | 0.257 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +31.41% | 0.083 | 0.446 | 0.466 |
| e-means: mass no, revival no, final means no | +117.34% | 0.048 | 0.225 | 0.262 |
| e-means: mass no, revival no, final means no + lists rebuilt | +31.96% | 0.081 | 0.453 | 0.475 |
| e-means: mass yes, revival yes, final means yes | +59.19% | 0.225 | 0.562 | 0.615 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +18.45% | 0.243 | 0.822 | 0.829 |
| e-means: mass yes, revival yes, final means no | +2.29% | 0.548 | 0.931 | 0.922 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +1.97% | 0.556 | 0.935 | 0.929 |
| e-means: mass yes, revival no, final means yes | +59.09% | 0.225 | 0.562 | 0.614 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +18.42% | 0.241 | 0.822 | 0.829 |
| e-means: mass yes, revival no, final means no | +2.24% | 0.548 | 0.931 | 0.922 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +1.97% | 0.556 | 0.935 | 0.929 |
| mini-batch k-means from the list sizes | +2.16% | 0.548 | 0.930 | 0.921 |
| mini-batch k-means from the list sizes + lists rebuilt | +1.96% | 0.554 | 0.934 | 0.926 |
| e-means: mass 0.2, step/4, no revival, no final means | +4.24% | 0.541 | 0.927 | 0.921 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +2.95% | 0.561 | 0.937 | 0.933 |
| warm start, 1 epoch per round | +2.46% | 0.560 | 0.934 | 0.934 |
| warm start, 3 epochs per round | +0.30% | 0.600 | 0.943 | 0.942 |
| warm start with steady-state mass, 3 epochs per round | +0.21% | 0.600 | 0.943 | 0.942 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.21% | 0.602 | 0.943 | 0.943 |
| from scratch, 1 epoch | +3.05% | 0.556 | 0.934 | 0.934 |
| from scratch, 3 epochs | +0.47% | 0.598 | 0.943 | 0.943 |
| from scratch, 10 epochs (reference) | +0.00% | 0.605 | 0.945 | 0.946 |
| never update, texts in random order (no-drift control) | +2.04% | 0.581 | 0.940 | — |
