Dataset: news. One update of 10000 texts, lists rebuilt.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

| unused_threshold | Naive use | With initial mass and moving average |
|---|---|---|
| None | 0.512 [0.512; 0.513] | 0.723 [0.710; 0.724] |
| 0.1 | 0.431 [0.430; 0.445] | 0.827 [0.825; 0.830] |
| 0 | 0.456 [0.423; 0.468] | 0.827 [0.825; 0.830] |
