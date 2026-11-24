Dataset: news, 384 dimensions.
Initial index: 100000 texts, from 2012-01-28 to 2015-02-08.
10 rounds of 10000 texts, up to 2019-09-01. 2048 lists, 3 algorithm seeds.
Recall@10 reading 0.1% and 1% of the index. Median over 3 seeds. The intervals are in results/SUMMARY.md.


### After 1 round (index up to 2015-06-06; 1536 queries, of which 146 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +0.76% | 0.487 | 0.828 | 0.807 |
| Faiss 1.16.0 e-means, default settings | +119.61% | 0.061 | 0.144 | 0.259 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +28.92% | 0.120 | 0.416 | 0.512 |
| e-means: mass no, revival yes, final means yes | +117.65% | 0.065 | 0.154 | 0.247 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +28.58% | 0.125 | 0.430 | 0.537 |
| e-means: mass no, revival yes, final means no | +121.55% | 0.047 | 0.131 | 0.232 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +29.51% | 0.133 | 0.440 | 0.545 |
| e-means: mass no, revival no, final means yes | +91.85% | 0.121 | 0.251 | 0.323 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +25.92% | 0.149 | 0.451 | 0.527 |
| e-means: mass no, revival no, final means no | +92.22% | 0.119 | 0.248 | 0.319 |
| e-means: mass no, revival no, final means no + lists rebuilt | +26.69% | 0.147 | 0.446 | 0.521 |
| e-means: mass yes, revival yes, final means yes | +26.94% | 0.372 | 0.680 | 0.716 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +12.91% | 0.372 | 0.747 | 0.757 |
| e-means: mass yes, revival yes, final means no | +0.57% | 0.487 | 0.828 | 0.809 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +0.55% | 0.489 | 0.827 | 0.806 |
| e-means: mass yes, revival no, final means yes | +26.94% | 0.372 | 0.679 | 0.715 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +12.93% | 0.372 | 0.746 | 0.757 |
| e-means: mass yes, revival no, final means no | +0.56% | 0.487 | 0.828 | 0.809 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +0.55% | 0.489 | 0.827 | 0.806 |
| mini-batch k-means from the list sizes | +0.53% | 0.488 | 0.827 | 0.808 |
| mini-batch k-means from the list sizes + lists rebuilt | +0.52% | 0.489 | 0.828 | 0.806 |
| e-means: mass 0.2, step/4, no revival, no final means | +1.28% | 0.483 | 0.825 | 0.805 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +1.15% | 0.485 | 0.824 | 0.804 |
| warm start, 1 epoch per round | +4.14% | 0.440 | 0.798 | 0.772 |
| warm start, 3 epochs per round | +0.60% | 0.490 | 0.826 | 0.806 |
| warm start with steady-state mass, 3 epochs per round | +0.23% | 0.491 | 0.828 | 0.805 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.36% | 0.491 | 0.828 | 0.804 |
| from scratch, 1 epoch | +4.98% | 0.429 | 0.798 | 0.779 |
| from scratch, 3 epochs | +0.94% | 0.485 | 0.825 | 0.808 |
| from scratch, 10 epochs (reference) | +0.00% | 0.501 | 0.834 | 0.817 |

### After 5 rounds (index up to 2016-09-10; 2136 queries, of which 746 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +3.19% | 0.461 | 0.806 | 0.758 |
| Faiss 1.16.0 e-means, default settings | +146.77% | 0.032 | 0.070 | 0.129 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +28.29% | 0.147 | 0.464 | 0.547 |
| e-means: mass no, revival yes, final means yes | +146.55% | 0.032 | 0.072 | 0.136 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +28.39% | 0.134 | 0.468 | 0.552 |
| e-means: mass no, revival yes, final means no | +135.81% | 0.028 | 0.067 | 0.118 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +28.74% | 0.144 | 0.473 | 0.552 |
| e-means: mass no, revival no, final means yes | +102.49% | 0.044 | 0.163 | 0.252 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +33.97% | 0.064 | 0.252 | 0.325 |
| e-means: mass no, revival no, final means no | +102.05% | 0.045 | 0.160 | 0.255 |
| e-means: mass no, revival no, final means no + lists rebuilt | +33.84% | 0.062 | 0.249 | 0.313 |
| e-means: mass yes, revival yes, final means yes | +59.29% | 0.189 | 0.438 | 0.571 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +22.33% | 0.198 | 0.577 | 0.643 |
| e-means: mass yes, revival yes, final means no | +1.86% | 0.473 | 0.819 | 0.787 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +1.62% | 0.479 | 0.822 | 0.794 |
| e-means: mass yes, revival no, final means yes | +59.39% | 0.189 | 0.435 | 0.570 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +22.29% | 0.198 | 0.576 | 0.647 |
| e-means: mass yes, revival no, final means no | +1.79% | 0.473 | 0.819 | 0.787 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +1.62% | 0.479 | 0.822 | 0.792 |
| mini-batch k-means from the list sizes | +1.73% | 0.474 | 0.817 | 0.783 |
| mini-batch k-means from the list sizes + lists rebuilt | +1.60% | 0.478 | 0.819 | 0.788 |
| e-means: mass 0.2, step/4, no revival, no final means | +3.47% | 0.470 | 0.818 | 0.790 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +2.58% | 0.479 | 0.823 | 0.799 |
| warm start, 1 epoch per round | +3.25% | 0.467 | 0.811 | 0.797 |
| warm start, 3 epochs per round | +0.53% | 0.510 | 0.834 | 0.823 |
| warm start with steady-state mass, 3 epochs per round | +0.24% | 0.512 | 0.834 | 0.819 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.33% | 0.511 | 0.835 | 0.821 |
| from scratch, 1 epoch | +4.15% | 0.456 | 0.810 | 0.801 |
| from scratch, 3 epochs | +0.80% | 0.507 | 0.833 | 0.819 |
| from scratch, 10 epochs (reference) | +0.00% | 0.524 | 0.840 | 0.832 |

### After 10 rounds (index up to 2019-09-01; 2898 queries, of which 1508 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +5.61% | 0.429 | 0.781 | 0.728 |
| Faiss 1.16.0 e-means, default settings | +145.10% | 0.024 | 0.052 | 0.079 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +32.87% | 0.140 | 0.433 | 0.503 |
| e-means: mass no, revival yes, final means yes | +143.66% | 0.024 | 0.053 | 0.080 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +32.81% | 0.142 | 0.448 | 0.514 |
| e-means: mass no, revival yes, final means no | +135.27% | 0.021 | 0.048 | 0.070 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +31.60% | 0.144 | 0.449 | 0.526 |
| e-means: mass no, revival no, final means yes | +98.63% | 0.035 | 0.143 | 0.196 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +37.21% | 0.064 | 0.220 | 0.245 |
| e-means: mass no, revival no, final means no | +100.63% | 0.036 | 0.142 | 0.192 |
| e-means: mass no, revival no, final means no + lists rebuilt | +37.19% | 0.065 | 0.233 | 0.258 |
| e-means: mass yes, revival yes, final means yes | +62.74% | 0.139 | 0.409 | 0.509 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +25.18% | 0.164 | 0.550 | 0.603 |
| e-means: mass yes, revival yes, final means no | +2.96% | 0.452 | 0.807 | 0.770 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +2.53% | 0.459 | 0.812 | 0.779 |
| e-means: mass yes, revival no, final means yes | +62.47% | 0.139 | 0.412 | 0.512 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +25.41% | 0.158 | 0.546 | 0.598 |
| e-means: mass yes, revival no, final means no | +2.90% | 0.451 | 0.807 | 0.768 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +2.56% | 0.458 | 0.811 | 0.777 |
| mini-batch k-means from the list sizes | +2.84% | 0.451 | 0.805 | 0.764 |
| mini-batch k-means from the list sizes + lists rebuilt | +2.59% | 0.457 | 0.810 | 0.773 |
| e-means: mass 0.2, step/4, no revival, no final means | +4.87% | 0.450 | 0.807 | 0.776 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +3.30% | 0.468 | 0.818 | 0.795 |
| warm start, 1 epoch per round | +2.64% | 0.493 | 0.824 | 0.812 |
| warm start, 3 epochs per round | +0.34% | 0.531 | 0.840 | 0.829 |
| warm start with steady-state mass, 3 epochs per round | +0.09% | 0.534 | 0.840 | 0.828 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.14% | 0.533 | 0.838 | 0.825 |
| from scratch, 1 epoch | +3.33% | 0.479 | 0.822 | 0.811 |
| from scratch, 3 epochs | +0.58% | 0.526 | 0.838 | 0.828 |
| from scratch, 10 epochs (reference) | +0.00% | 0.536 | 0.843 | 0.835 |
| never update, texts in random order (no-drift control) | +1.99% | 0.504 | 0.831 | — |
