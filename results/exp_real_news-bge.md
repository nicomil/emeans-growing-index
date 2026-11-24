Dataset: news-bge, 768 dimensions.
Initial index: 100000 texts, from 2012-01-28 to 2015-02-08.
10 rounds of 10000 texts, up to 2019-09-01. 2048 lists, 3 algorithm seeds.
Recall@10 reading 0.1% and 1% of the index. Median over 3 seeds. The intervals are in results/SUMMARY.md.


### After 1 round (index up to 2015-06-06; 1536 queries, of which 146 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +0.84% | 0.428 | 0.792 | 0.768 |
| Faiss 1.16.0 e-means, default settings | +118.80% | 0.041 | 0.114 | 0.218 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +26.96% | 0.076 | 0.332 | 0.445 |
| e-means: mass no, revival yes, final means yes | +117.38% | 0.044 | 0.115 | 0.228 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +26.97% | 0.081 | 0.337 | 0.442 |
| e-means: mass no, revival yes, final means no | +119.69% | 0.031 | 0.097 | 0.199 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +27.90% | 0.089 | 0.352 | 0.447 |
| e-means: mass no, revival no, final means yes | +93.31% | 0.084 | 0.186 | 0.292 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +23.90% | 0.099 | 0.364 | 0.431 |
| e-means: mass no, revival no, final means no | +93.56% | 0.084 | 0.183 | 0.284 |
| e-means: mass no, revival no, final means no + lists rebuilt | +24.52% | 0.099 | 0.356 | 0.428 |
| e-means: mass yes, revival yes, final means yes | +27.66% | 0.314 | 0.622 | 0.668 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +11.40% | 0.310 | 0.701 | 0.710 |
| e-means: mass yes, revival yes, final means no | +0.62% | 0.430 | 0.792 | 0.771 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +0.60% | 0.431 | 0.792 | 0.773 |
| e-means: mass yes, revival no, final means yes | +27.65% | 0.314 | 0.622 | 0.668 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +11.43% | 0.310 | 0.701 | 0.710 |
| e-means: mass yes, revival no, final means no | +0.61% | 0.430 | 0.792 | 0.771 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +0.60% | 0.431 | 0.792 | 0.773 |
| mini-batch k-means from the list sizes | +0.58% | 0.430 | 0.793 | 0.772 |
| mini-batch k-means from the list sizes + lists rebuilt | +0.57% | 0.430 | 0.793 | 0.773 |
| e-means: mass 0.2, step/4, no revival, no final means | +1.32% | 0.428 | 0.792 | 0.765 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +1.19% | 0.432 | 0.792 | 0.771 |
| warm start, 1 epoch per round | +4.11% | 0.375 | 0.760 | 0.744 |
| warm start, 3 epochs per round | +0.64% | 0.430 | 0.789 | 0.768 |
| warm start with steady-state mass, 3 epochs per round | +0.35% | 0.438 | 0.793 | 0.772 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.48% | 0.437 | 0.792 | 0.773 |
| from scratch, 1 epoch | +4.77% | 0.376 | 0.757 | 0.752 |
| from scratch, 3 epochs | +1.01% | 0.425 | 0.787 | 0.773 |
| from scratch, 10 epochs (reference) | +0.00% | 0.444 | 0.798 | 0.775 |

### After 5 rounds (index up to 2016-09-10; 2136 queries, of which 746 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +3.98% | 0.404 | 0.773 | 0.718 |
| Faiss 1.16.0 e-means, default settings | +138.54% | 0.026 | 0.061 | 0.124 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +26.26% | 0.111 | 0.396 | 0.510 |
| e-means: mass no, revival yes, final means yes | +138.75% | 0.027 | 0.062 | 0.119 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +25.93% | 0.109 | 0.411 | 0.531 |
| e-means: mass no, revival yes, final means no | +131.06% | 0.022 | 0.056 | 0.108 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +26.12% | 0.116 | 0.418 | 0.513 |
| e-means: mass no, revival no, final means yes | +97.48% | 0.027 | 0.127 | 0.228 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +31.60% | 0.038 | 0.173 | 0.245 |
| e-means: mass no, revival no, final means no | +97.54% | 0.028 | 0.129 | 0.230 |
| e-means: mass no, revival no, final means no + lists rebuilt | +32.04% | 0.037 | 0.174 | 0.241 |
| e-means: mass yes, revival yes, final means yes | +58.79% | 0.155 | 0.388 | 0.530 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +20.35% | 0.169 | 0.536 | 0.624 |
| e-means: mass yes, revival yes, final means no | +2.18% | 0.420 | 0.788 | 0.752 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +1.93% | 0.425 | 0.793 | 0.763 |
| e-means: mass yes, revival no, final means yes | +58.58% | 0.157 | 0.391 | 0.529 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +20.24% | 0.168 | 0.537 | 0.623 |
| e-means: mass yes, revival no, final means no | +2.14% | 0.419 | 0.789 | 0.752 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +1.93% | 0.425 | 0.793 | 0.763 |
| mini-batch k-means from the list sizes | +2.07% | 0.420 | 0.788 | 0.748 |
| mini-batch k-means from the list sizes + lists rebuilt | +1.91% | 0.424 | 0.793 | 0.759 |
| e-means: mass 0.2, step/4, no revival, no final means | +3.84% | 0.417 | 0.789 | 0.767 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +2.81% | 0.429 | 0.797 | 0.786 |
| warm start, 1 epoch per round | +3.29% | 0.417 | 0.785 | 0.784 |
| warm start, 3 epochs per round | +0.56% | 0.457 | 0.807 | 0.806 |
| warm start with steady-state mass, 3 epochs per round | +0.23% | 0.470 | 0.811 | 0.808 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.37% | 0.466 | 0.812 | 0.806 |
| from scratch, 1 epoch | +4.35% | 0.403 | 0.781 | 0.786 |
| from scratch, 3 epochs | +0.73% | 0.456 | 0.808 | 0.810 |
| from scratch, 10 epochs (reference) | +0.00% | 0.475 | 0.814 | 0.817 |

### After 10 rounds (index up to 2019-09-01; 2898 queries, of which 1508 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +6.95% | 0.376 | 0.745 | 0.682 |
| Faiss 1.16.0 e-means, default settings | +136.03% | 0.022 | 0.049 | 0.077 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +30.53% | 0.115 | 0.388 | 0.484 |
| e-means: mass no, revival yes, final means yes | +135.57% | 0.021 | 0.047 | 0.075 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +30.88% | 0.115 | 0.385 | 0.475 |
| e-means: mass no, revival yes, final means no | +128.24% | 0.019 | 0.045 | 0.071 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +29.76% | 0.121 | 0.390 | 0.492 |
| e-means: mass no, revival no, final means yes | +91.29% | 0.025 | 0.103 | 0.148 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +35.32% | 0.040 | 0.148 | 0.166 |
| e-means: mass no, revival no, final means no | +92.90% | 0.026 | 0.102 | 0.143 |
| e-means: mass no, revival no, final means no + lists rebuilt | +35.66% | 0.038 | 0.134 | 0.153 |
| e-means: mass yes, revival yes, final means yes | +61.42% | 0.118 | 0.364 | 0.476 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +23.53% | 0.137 | 0.512 | 0.572 |
| e-means: mass yes, revival yes, final means no | +3.52% | 0.400 | 0.773 | 0.729 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +2.93% | 0.411 | 0.786 | 0.749 |
| e-means: mass yes, revival no, final means yes | +61.34% | 0.117 | 0.365 | 0.477 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +23.47% | 0.138 | 0.504 | 0.569 |
| e-means: mass yes, revival no, final means no | +3.43% | 0.399 | 0.773 | 0.727 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +2.99% | 0.409 | 0.783 | 0.744 |
| mini-batch k-means from the list sizes | +3.36% | 0.396 | 0.770 | 0.723 |
| mini-batch k-means from the list sizes + lists rebuilt | +3.04% | 0.405 | 0.780 | 0.738 |
| e-means: mass 0.2, step/4, no revival, no final means | +5.26% | 0.400 | 0.776 | 0.741 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +3.54% | 0.421 | 0.794 | 0.771 |
| warm start, 1 epoch per round | +2.69% | 0.441 | 0.797 | 0.792 |
| warm start, 3 epochs per round | +0.39% | 0.476 | 0.815 | 0.811 |
| warm start with steady-state mass, 3 epochs per round | +0.05% | 0.487 | 0.819 | 0.810 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.13% | 0.489 | 0.820 | 0.813 |
| from scratch, 1 epoch | +3.39% | 0.427 | 0.792 | 0.787 |
| from scratch, 3 epochs | +0.59% | 0.476 | 0.814 | 0.810 |
| from scratch, 10 epochs (reference) | +0.00% | 0.487 | 0.822 | 0.819 |
| never update, texts in random order (no-drift control) | +2.06% | 0.456 | 0.807 | — |
