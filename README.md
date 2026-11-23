# e-means e gli indici che cambiano: aggiornare o ricalcolare?

Studio indipendente di [e-means](https://arxiv.org/abs/2611.09501), la variante di k-means pubblicata da Meta FAIR nel novembre 2026 e distribuita in Faiss 1.16.0, in una situazione che il paper non tratta: un indice vettoriale a cluster (IVF) che riceve documenti nuovi nel tempo.

Il brief del progetto è in `_bmad-output/planning-artifacts/briefs/`, i risultati in `results/SINTESI.md`, il percorso passo per passo, con le revisioni, in `_bmad-output/implementation-artifacts/`.

## Cosa c'è

| File | Cosa fa |
|---|---|
| `emeans.py` | e-means in un file NumPy breve, con ciò che Faiss non espone: massa iniziale dei centroidi e medie finali disattivabili |
| `test_emeans.py` | Test, compreso il confronto con l'implementazione di Faiss |
| `demo_2d.py` | Animazione dei centroidi su punti in due dimensioni |
| `exp_warm.py`, `exp_new_only.py`, `exp_rule.py`, `exp_sequence.py` | Esperimenti su dati sintetici con deriva controllata (passi 3, 4, 4b, D) |
| `embed_corpus.py` | Scarica un corpus con date e ne calcola gli embedding |
| `exp_real.py` | Strategie di aggiornamento di un indice su embedding veri: errore e recall |
| `bench_rebuild.py` | Tempi del ricalcolo completo, e-means contro k-means classico |
| `check_recall_vs_faiss.py` | Verifica che il recall calcolato qui coincida con quello di un indice IVF di Faiss |
| `check_faiss_naive.py` | L'aggiornamento ingenuo e la sua correzione, fatti con il codice di Faiss |
| `check_naive_baselines.py` | Lo stesso aggiornamento con k-means e con due dimensioni di aggiornamento |
| `analyze.py` | Sintesi con intervalli di confidenza |
| `docs/repro_emeans_init_centroids.py` | Riproduzione minima, autonoma, del comportamento di `init_centroids` |

## Rifare i risultati

Serve [uv](https://docs.astral.sh/uv/). Le dipendenze si installano da sole al primo comando.

```bash
uv run pytest -q                                   # test, pochi secondi

# dati sintetici
uv run exp_warm.py                                 # circa 1 minuto
uv run exp_new_only.py sovrapposti                 # anche: netti, senza-deriva; 3-4 minuti l'uno
uv run exp_rule.py sovrapposti > results/exp_rule_sovrapposti.md
uv run exp_rule.py netti > results/exp_rule_netti.md
uv run exp_sequence.py > results/exp_sequence.md   # richiede il comando precedente

# dati veri: prima gli embedding, una volta per insieme di dati
uv run --group real embed_corpus.py news           # notizie, modello a 384 dimensioni: pochi minuti
uv run --group real embed_corpus.py arxiv          # abstract, scarica 1,4 GB: circa 15 minuti
uv run --group real embed_corpus.py news bge       # modello a 768 dimensioni: circa 30 minuti
uv run --group real embed_corpus.py arxiv bge      # alcune ore su un portatile

# poi, per ogni insieme di dati (news, arxiv, news-bge, arxiv-bge)
uv run exp_real.py news > results/exp_real_news.md                  # circa 30 minuti
uv run check_recall_vs_faiss.py news > results/check_recall_news.md
uv run bench_rebuild.py news > results/bench_rebuild_news.md        # da solo, a macchina libera
uv run check_faiss_naive.py news > results/check_faiss_naive_news.md
uv run check_naive_baselines.py news > results/check_naive_baselines_news.md
uv run analyze.py > results/SINTESI.md
```

`run_night2.sh` esegue la parte sui dati veri in fila, un lavoro alla volta.

Gli embedding finiscono in `data/`, che non è sotto controllo di versione: ogni file pesa da 300 a 650 MB.

## Dati e modelli

- Notizie: [`heegyu/news-category-dataset`](https://huggingface.co/datasets/heegyu/news-category-dataset), titoli e sommari di HuffPost, 2012-2022.
- Abstract: [`gfissore/arxiv-abstracts-2021`](https://huggingface.co/datasets/gfissore/arxiv-abstracts-2021), 210.000 articoli estratti a caso tra il 2007 e il 2021.
- Embedding: [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) e [`bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5).

Le revisioni di dataset e modelli non sono fissate: scaricandoli in futuro i numeri possono cambiare leggermente.

## Limiti da tenere presenti

- Indici da 200.000 vettori su un portatile. A scale molto più grandi il costo del ricalcolo completo cresce e le conclusioni pratiche possono cambiare.
- Le interrogazioni sono testi del corpus tenuti fuori dall'indice, non domande di utenti.
- I confronti sono con metodi semplici, non con quelli della letteratura sulla deriva degli indici (DeDrift, Ada-IVF, SPFresh).
- Faiss 1.16.0. Il ramo principale di Faiss ha poi cambiato la rianimazione dei cluster: quella parte non è stata rieseguita sul codice più recente.
