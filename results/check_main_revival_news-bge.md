Dataset: news-bge. One update of 10000 texts, lists rebuilt.
Recall@10 reading 1% of the index, median [min; max] over 3 seeds.

| unused_threshold | Naive use | With initial mass and moving average |
|---|---|---|
| None | 0.421 [0.403; 0.442] | 0.665 [0.662; 0.676] |
| 0.1 | 0.336 [0.329; 0.338] | 0.792 [0.791; 0.794] |
| 0 | 0.367 [0.348; 0.380] | 0.792 [0.791; 0.794] |
