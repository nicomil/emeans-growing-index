Dataset: arxiv-bge, 768 dimensions.
Initial index: 100000 texts, from 2007-04-01 to 2016-08-01.
10 rounds of 10000 texts, up to 2021-09-01. 2048 lists, 3 algorithm seeds.
Recall@10 reading 0.1% and 1% of the index. Median over 3 seeds. The intervals are in results/SUMMARY.md.


### After 1 round (index up to 2017-04-01; 1534 queries, of which 145 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +0.64% | 0.565 | 0.937 | 0.943 |
| Faiss 1.16.0 e-means, default settings | +137.16% | 0.077 | 0.223 | 0.272 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +25.68% | 0.160 | 0.654 | 0.671 |
| e-means: mass no, revival yes, final means yes | +139.43% | 0.084 | 0.234 | 0.267 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +25.05% | 0.171 | 0.665 | 0.682 |
| e-means: mass no, revival yes, final means no | +155.24% | 0.061 | 0.184 | 0.221 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +25.96% | 0.190 | 0.678 | 0.688 |
| e-means: mass no, revival no, final means yes | +88.78% | 0.133 | 0.371 | 0.381 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +23.78% | 0.162 | 0.670 | 0.664 |
| e-means: mass no, revival no, final means no | +89.20% | 0.132 | 0.377 | 0.389 |
| e-means: mass no, revival no, final means no + lists rebuilt | +24.61% | 0.159 | 0.660 | 0.659 |
| e-means: mass yes, revival yes, final means yes | +25.87% | 0.448 | 0.831 | 0.834 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +15.72% | 0.442 | 0.892 | 0.894 |
| e-means: mass yes, revival yes, final means no | +0.46% | 0.567 | 0.937 | 0.943 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +0.44% | 0.568 | 0.937 | 0.943 |
| e-means: mass yes, revival no, final means yes | +25.85% | 0.448 | 0.831 | 0.834 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +15.72% | 0.442 | 0.892 | 0.894 |
| e-means: mass yes, revival no, final means no | +0.45% | 0.567 | 0.937 | 0.943 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +0.44% | 0.568 | 0.937 | 0.943 |
| mini-batch k-means from the list sizes | +0.42% | 0.567 | 0.937 | 0.942 |
| mini-batch k-means from the list sizes + lists rebuilt | +0.41% | 0.568 | 0.937 | 0.943 |
| e-means: mass 0.2, step/4, no revival, no final means | +1.26% | 0.563 | 0.936 | 0.941 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +1.15% | 0.565 | 0.937 | 0.942 |
| warm start, 1 epoch per round | +3.90% | 0.515 | 0.925 | 0.926 |
| warm start, 3 epochs per round | +0.52% | 0.568 | 0.938 | 0.941 |
| warm start with steady-state mass, 3 epochs per round | +0.19% | 0.573 | 0.937 | 0.939 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.31% | 0.571 | 0.935 | 0.934 |
| from scratch, 1 epoch | +4.38% | 0.508 | 0.922 | 0.923 |
| from scratch, 3 epochs | +0.73% | 0.561 | 0.937 | 0.930 |
| from scratch, 10 epochs (reference) | +0.00% | 0.582 | 0.938 | 0.941 |

### After 5 rounds (index up to 2019-07-01; 2145 queries, of which 756 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +2.29% | 0.560 | 0.934 | 0.928 |
| Faiss 1.16.0 e-means, default settings | +210.34% | 0.038 | 0.083 | 0.106 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +23.05% | 0.206 | 0.750 | 0.756 |
| e-means: mass no, revival yes, final means yes | +208.67% | 0.036 | 0.081 | 0.105 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +22.49% | 0.214 | 0.763 | 0.766 |
| e-means: mass no, revival yes, final means no | +198.08% | 0.030 | 0.068 | 0.086 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +23.37% | 0.231 | 0.751 | 0.758 |
| e-means: mass no, revival no, final means yes | +107.60% | 0.051 | 0.233 | 0.272 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +30.63% | 0.076 | 0.456 | 0.482 |
| e-means: mass no, revival no, final means no | +107.70% | 0.050 | 0.238 | 0.277 |
| e-means: mass no, revival no, final means no + lists rebuilt | +30.75% | 0.073 | 0.445 | 0.464 |
| e-means: mass yes, revival yes, final means yes | +51.00% | 0.281 | 0.619 | 0.665 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +17.42% | 0.287 | 0.840 | 0.844 |
| e-means: mass yes, revival yes, final means no | +1.36% | 0.567 | 0.937 | 0.935 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +1.21% | 0.572 | 0.938 | 0.937 |
| e-means: mass yes, revival no, final means yes | +51.31% | 0.282 | 0.619 | 0.667 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +17.43% | 0.286 | 0.839 | 0.843 |
| e-means: mass yes, revival no, final means no | +1.32% | 0.567 | 0.937 | 0.935 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +1.21% | 0.572 | 0.938 | 0.937 |
| mini-batch k-means from the list sizes | +1.23% | 0.567 | 0.937 | 0.934 |
| mini-batch k-means from the list sizes + lists rebuilt | +1.16% | 0.571 | 0.938 | 0.936 |
| e-means: mass 0.2, step/4, no revival, no final means | +3.11% | 0.558 | 0.933 | 0.930 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +2.43% | 0.569 | 0.937 | 0.937 |
| warm start, 1 epoch per round | +3.16% | 0.547 | 0.930 | 0.928 |
| warm start, 3 epochs per round | +0.49% | 0.585 | 0.940 | 0.942 |
| warm start with steady-state mass, 3 epochs per round | +0.15% | 0.600 | 0.942 | 0.941 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.22% | 0.592 | 0.942 | 0.943 |
| from scratch, 1 epoch | +3.83% | 0.532 | 0.929 | 0.928 |
| from scratch, 3 epochs | +0.69% | 0.585 | 0.943 | 0.943 |
| from scratch, 10 epochs (reference) | +0.00% | 0.598 | 0.943 | 0.944 |

### After 10 rounds (index up to 2021-09-01; 2900 queries, of which 1511 from the added period)

| Strategy | Error in the lists | Recall, 0.1% read | Recall, 1% read | Recall 1%, added period |
|---|---|---|---|---|
| never update | +4.18% | 0.547 | 0.928 | 0.916 |
| Faiss 1.16.0 e-means, default settings | +211.46% | 0.029 | 0.064 | 0.079 |
| Faiss 1.16.0 e-means, default settings + lists rebuilt | +22.46% | 0.236 | 0.772 | 0.787 |
| e-means: mass no, revival yes, final means yes | +211.58% | 0.030 | 0.068 | 0.085 |
| e-means: mass no, revival yes, final means yes + lists rebuilt | +22.29% | 0.238 | 0.773 | 0.780 |
| e-means: mass no, revival yes, final means no | +205.19% | 0.025 | 0.057 | 0.072 |
| e-means: mass no, revival yes, final means no + lists rebuilt | +23.42% | 0.235 | 0.756 | 0.763 |
| e-means: mass no, revival no, final means yes | +114.40% | 0.043 | 0.223 | 0.265 |
| e-means: mass no, revival no, final means yes + lists rebuilt | +31.76% | 0.067 | 0.416 | 0.443 |
| e-means: mass no, revival no, final means no | +111.94% | 0.043 | 0.220 | 0.260 |
| e-means: mass no, revival no, final means no + lists rebuilt | +31.97% | 0.066 | 0.417 | 0.443 |
| e-means: mass yes, revival yes, final means yes | +56.68% | 0.223 | 0.571 | 0.633 |
| e-means: mass yes, revival yes, final means yes + lists rebuilt | +18.11% | 0.241 | 0.830 | 0.838 |
| e-means: mass yes, revival yes, final means no | +2.16% | 0.559 | 0.937 | 0.932 |
| e-means: mass yes, revival yes, final means no + lists rebuilt | +1.84% | 0.569 | 0.940 | 0.936 |
| e-means: mass yes, revival no, final means yes | +56.29% | 0.223 | 0.568 | 0.631 |
| e-means: mass yes, revival no, final means yes + lists rebuilt | +18.10% | 0.236 | 0.831 | 0.835 |
| e-means: mass yes, revival no, final means no | +2.13% | 0.559 | 0.938 | 0.932 |
| e-means: mass yes, revival no, final means no + lists rebuilt | +1.87% | 0.568 | 0.940 | 0.937 |
| mini-batch k-means from the list sizes | +2.04% | 0.559 | 0.937 | 0.931 |
| mini-batch k-means from the list sizes + lists rebuilt | +1.85% | 0.566 | 0.939 | 0.935 |
| e-means: mass 0.2, step/4, no revival, no final means | +4.02% | 0.551 | 0.931 | 0.926 |
| e-means: mass 0.2, step/4, no revival, no final means + lists rebuilt | +2.83% | 0.572 | 0.940 | 0.939 |
| warm start, 1 epoch per round | +2.42% | 0.574 | 0.938 | 0.940 |
| warm start, 3 epochs per round | +0.27% | 0.614 | 0.947 | 0.946 |
| warm start with steady-state mass, 3 epochs per round | +0.10% | 0.614 | 0.947 | 0.947 |
| warm start with steady-state mass, no final means, 3 epochs per round | +0.13% | 0.614 | 0.946 | 0.947 |
| from scratch, 1 epoch | +2.93% | 0.566 | 0.937 | 0.938 |
| from scratch, 3 epochs | +0.43% | 0.606 | 0.946 | 0.945 |
| from scratch, 10 epochs (reference) | +0.00% | 0.619 | 0.948 | 0.948 |
| never update, texts in random order (no-drift control) | +1.95% | 0.593 | 0.943 | — |
