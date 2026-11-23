Insieme di dati: arxiv. 200000 vettori a 384 dimensioni, 2048 centroidi, 2900 testi tenuti fuori.
Macchina: Apple M1, macOS-27.2.1-arm64-arm-64bit. Faiss 1.16.0 con 8 thread, NumPy 2.5.5, Python 3.12.11.
6 ripetizioni in ordine alternato. Tempo: mediana [minimo; massimo]. Le altre colonne: mediana.
Carico della macchina prima delle misure (media a 1 minuto): mediana 2.2, massimo 5.0. Comprende il calcolo del recall della misura precedente, che usa un solo core.

| Metodo | Passate | Tempo | Errore di addestramento | Errore sui testi tenuti fuori | Recall, 0,1% letto | Recall, 1% letto |
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
