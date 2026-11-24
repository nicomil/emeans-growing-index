Dataset: news-bge. 200000 vectors of 768 dimensions, 2048 centroids, 2898 held-out texts.
Machine: Apple M1, macOS-27.2.1-arm64-arm-64bit. Faiss 1.16.0 with 8 threads, NumPy 2.5.5, Python 3.12.11.
6 repetitions in alternating order. Time: median [minimum; maximum]. The other columns: median.
Load of the machine before the measurements (1-minute average): median 2.4, maximum 4.0. It includes the recall computation of the previous measurement, which uses a single core.

| Method | Passes | Time | Training error | Error on the held-out texts | Recall, 0.1% read | Recall, 1% read |
|---|---|---|---|---|---|---|
| e-means | 1 | 2.3 s [2.3; 2.3] | 0.4196 | 0.4293 | 0.429 | 0.791 |
| e-means | 2 | 4.5 s [4.3; 4.7] | 0.4101 | 0.4226 | 0.464 | 0.811 |
| e-means | 3 | 6.7 s [6.4; 6.9] | 0.4079 | 0.4204 | 0.476 | 0.815 |
| e-means | 5 | 10.9 s [10.6; 11.0] | 0.4066 | 0.4196 | 0.484 | 0.819 |
| e-means | 10 | 21.8 s [21.3; 21.9] | 0.4057 | 0.4191 | 0.489 | 0.820 |
| k-means | 3 | 3.6 s [3.5; 3.7] | 0.4177 | 0.4288 | 0.430 | 0.807 |
| k-means | 5 | 5.9 s [5.7; 6.0] | 0.4134 | 0.4253 | 0.452 | 0.815 |
| k-means | 10 | 11.8 s [11.4; 12.0] | 0.4101 | 0.4227 | 0.467 | 0.820 |
| k-means | 12 | 14.3 s [13.7; 14.4] | 0.4096 | 0.4224 | 0.470 | 0.821 |
| k-means | 15 | 17.8 s [17.2; 18.0] | 0.4092 | 0.4220 | 0.472 | 0.821 |
| k-means | 20 | 23.7 s [23.3; 24.0] | 0.4088 | 0.4217 | 0.474 | 0.821 |
| k-means | 25 | 29.7 s [29.1; 30.0] | 0.4086 | 0.4215 | 0.474 | 0.821 |
