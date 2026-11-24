Dataset: arxiv. 200000 vectors of 384 dimensions, 2048 centroids, 2900 held-out texts.
Machine: Apple M1, macOS-27.2.1-arm64-arm-64bit. Faiss 1.16.0 with 8 threads, NumPy 2.5.5, Python 3.12.11.
6 repetitions in alternating order. Time: median [minimum; maximum]. The other columns: median.
Load of the machine before the measurements (1-minute average): median 2.2, maximum 5.0. It includes the recall computation of the previous measurement, which uses a single core.

| Method | Passes | Time | Training error | Error on the held-out texts | Recall, 0.1% read | Recall, 1% read |
|---|---|---|---|---|---|---|
| e-means | 1 | 1.5 s [1.5; 1.5] | 0.5181 | 0.5278 | 0.554 | 0.933 |
| e-means | 2 | 2.9 s [2.8; 2.9] | 0.5075 | 0.5202 | 0.587 | 0.940 |
| e-means | 3 | 4.3 s [4.3; 4.3] | 0.5053 | 0.5177 | 0.596 | 0.943 |
| e-means | 5 | 7.1 s [7.1; 7.2] | 0.5039 | 0.5174 | 0.602 | 0.945 |
| e-means | 10 | 14.1 s [14.0; 14.2] | 0.5029 | 0.5164 | 0.609 | 0.945 |
| k-means | 3 | 2.7 s [2.7; 2.8] | 0.5180 | 0.5293 | 0.549 | 0.936 |
| k-means | 5 | 4.5 s [4.5; 4.6] | 0.5126 | 0.5247 | 0.573 | 0.940 |
| k-means | 10 | 9.1 s [9.1; 9.5] | 0.5083 | 0.5213 | 0.589 | 0.943 |
| k-means | 12 | 10.9 s [10.8; 11.0] | 0.5076 | 0.5206 | 0.592 | 0.944 |
| k-means | 15 | 13.6 s [13.5; 13.7] | 0.5070 | 0.5199 | 0.596 | 0.944 |
| k-means | 20 | 18.2 s [18.1; 18.2] | 0.5064 | 0.5194 | 0.597 | 0.944 |
| k-means | 25 | 22.7 s [22.6; 22.8] | 0.5061 | 0.5191 | 0.597 | 0.944 |
