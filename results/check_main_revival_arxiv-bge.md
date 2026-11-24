Dataset: arxiv-bge. One update of 10000 texts, lists rebuilt.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

| unused_threshold | Naive use | With initial mass and moving average |
|---|---|---|
| None | 0.785 [0.783; 0.790] | 0.891 [0.889; 0.894] |
| 0.1 | 0.681 [0.680; 0.681] | 0.937 [0.937; 0.938] |
| 0 | 0.692 [0.683; 0.700] | 0.937 [0.937; 0.938] |
