Dataset: news. 200000 vectors of 384 dimensions, 2048 centroids, 2898 held-out texts.
Machine: Apple M1, macOS-27.2.1-arm64-arm-64bit. Faiss 1.16.0 with 8 threads, NumPy 2.5.5, Python 3.12.11.
6 repetitions in alternating order. Time: median [minimum; maximum]. The other columns: median.
Load of the machine before the measurements (1-minute average): median 1.9, maximum 3.1. It includes the recall computation of the previous measurement, which uses a single core.

| Method | Passes | Time | Training error | Error on the held-out texts | Recall, 0.1% read | Recall, 1% read |
|---|---|---|---|---|---|---|
| e-means | 1 | 1.5 s [1.4; 1.5] | 0.6268 | 0.6395 | 0.479 | 0.818 |
| e-means | 2 | 2.9 s [2.8; 2.9] | 0.6128 | 0.6293 | 0.517 | 0.836 |
| e-means | 3 | 4.3 s [4.3; 4.4] | 0.6099 | 0.6270 | 0.525 | 0.838 |
| e-means | 5 | 7.1 s [7.1; 7.1] | 0.6080 | 0.6252 | 0.533 | 0.840 |
| e-means | 10 | 14.1 s [14.1; 14.2] | 0.6066 | 0.6237 | 0.537 | 0.842 |
| k-means | 3 | 2.7 s [2.7; 2.8] | 0.6264 | 0.6414 | 0.478 | 0.833 |
| k-means | 5 | 4.5 s [4.5; 4.6] | 0.6192 | 0.6351 | 0.501 | 0.838 |
| k-means | 10 | 9.1 s [9.1; 9.1] | 0.6136 | 0.6305 | 0.517 | 0.842 |
| k-means | 12 | 10.9 s [10.8; 10.9] | 0.6127 | 0.6299 | 0.522 | 0.843 |
| k-means | 15 | 13.6 s [13.6; 13.9] | 0.6119 | 0.6293 | 0.523 | 0.843 |
| k-means | 20 | 18.2 s [18.1; 18.2] | 0.6112 | 0.6288 | 0.526 | 0.843 |
| k-means | 25 | 22.6 s [22.5; 22.7] | 0.6109 | 0.6285 | 0.527 | 0.843 |
