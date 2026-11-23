Insieme di dati: arxiv-bge. 200000 vettori a 768 dimensioni, 2048 centroidi, 2900 testi tenuti fuori.
Macchina: Apple M1, macOS-27.2.1-arm64-arm-64bit. Faiss 1.16.0 con 8 thread, NumPy 2.5.5, Python 3.12.11.
6 ripetizioni in ordine alternato. Tempo: mediana [minimo; massimo]. Le altre colonne: mediana.
Carico della macchina prima delle misure (media a 1 minuto): mediana 2.1, massimo 5.5. Comprende il calcolo del recall della misura precedente, che usa un solo core.

| Metodo | Passate | Tempo | Errore di addestramento | Errore sui testi tenuti fuori | Recall, 0,1% letto | Recall, 1% letto |
|---|---|---|---|---|---|---|
| e-means | 1 | 2.2 s [2.2; 2.2] | 0.2470 | 0.2514 | 0.564 | 0.938 |
| e-means | 2 | 4.3 s [4.3; 4.3] | 0.2420 | 0.2476 | 0.600 | 0.945 |
| e-means | 3 | 6.4 s [6.4; 6.5] | 0.2410 | 0.2470 | 0.607 | 0.947 |
| e-means | 5 | 10.6 s [10.5; 10.7] | 0.2404 | 0.2466 | 0.611 | 0.948 |
| e-means | 10 | 21.1 s [20.8; 21.3] | 0.2400 | 0.2461 | 0.618 | 0.948 |
| k-means | 3 | 3.5 s [3.4; 3.6] | 0.2467 | 0.2515 | 0.557 | 0.940 |
| k-means | 5 | 5.8 s [5.7; 5.9] | 0.2443 | 0.2497 | 0.581 | 0.944 |
| k-means | 10 | 11.5 s [11.3; 12.0] | 0.2425 | 0.2482 | 0.597 | 0.946 |
| k-means | 12 | 13.8 s [13.5; 13.9] | 0.2422 | 0.2480 | 0.601 | 0.946 |
| k-means | 15 | 17.2 s [16.9; 17.5] | 0.2419 | 0.2478 | 0.602 | 0.947 |
| k-means | 20 | 23.0 s [22.5; 23.1] | 0.2417 | 0.2476 | 0.604 | 0.947 |
| k-means | 25 | 28.8 s [28.2; 28.9] | 0.2416 | 0.2476 | 0.605 | 0.947 |
