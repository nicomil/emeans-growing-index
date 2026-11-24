Dataset: arxiv. One update of 10000 texts, lists rebuilt.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

| unused_threshold | Naive use | With initial mass and moving average |
|---|---|---|
| None | 0.784 [0.775; 0.788] | 0.886 [0.884; 0.887] |
| 0.1 | 0.678 [0.669; 0.680] | 0.932 [0.931; 0.934] |
| 0 | 0.678 [0.671; 0.680] | 0.932 [0.931; 0.934] |
