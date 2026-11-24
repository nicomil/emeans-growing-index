# e-means e gli indici che cambiano: aggiornare o ricalcolare?

Studio indipendente di [e-means](https://arxiv.org/abs/2611.09501), la variante di k-means pubblicata da Meta FAIR nel novembre 2026 e distribuita in Faiss 1.16.0, in una situazione che il paper non tratta: un indice vettoriale a cluster (IVF) che riceve documenti nuovi nel tempo.

I risultati sono in `results/SINTESI.md`, il rapporto in `docs/RAPPORTO.md`. Il brief del progetto (`brief.md`) e il percorso passo per passo, con le revisioni, sono in `docs/percorso/`.

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
| `check_main_revival.py` | Sul ramo principale di Faiss: quanto dipende dalla rianimazione dei cluster |
| `exp_scale.py` | L'esperimento a 1,5 milioni di testi e 16.384 centroidi, con il solo codice di Faiss e il confronto con DeDrift |
| `bench_scale.py` | Tempi del ricalcolo completo a quella scala |
| `check_split.py` | Quanto pesano le scelte che il paper di DeDrift non fissa |
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

Per ripetere l'aggiornamento singolo sul ramo principale di Faiss serve compilarlo (CMake, SWIG, libomp) e usare quel Python al posto di `uv run`:

```bash
git clone https://github.com/facebookresearch/faiss.git vendor/faiss_src && cd vendor/faiss_src
uv venv ../faiss_venv --python 3.12 && uv pip install --python ../faiss_venv/bin/python numpy setuptools
cmake -B build -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_METAL=OFF -DFAISS_ENABLE_PYTHON=ON -DBUILD_TESTING=OFF \
  -DFAISS_OPT_LEVEL=generic -DPython_EXECUTABLE=$PWD/../faiss_venv/bin/python -DOpenMP_ROOT=$(brew --prefix libomp) .
cmake --build build -j4 --target faiss swigfaiss
(cd build/faiss/python && uv pip install --python ../../../../faiss_venv/bin/python .) && cd ../..
vendor/faiss_venv/bin/python check_naive_baselines.py news > results/check_naive_baselines_news_main.md
vendor/faiss_venv/bin/python check_main_revival.py news > results/check_main_revival_news.md
```

Scala grande (1,5 milioni di testi; servono circa 2 ore di embedding per arXiv, 1 per MS MARCO, e 16 GB di memoria):

```
uv run --group real embed_corpus.py arxiv-full
uv run --group real embed_corpus.py msmarco
uv run exp_scale.py arxiv-full 0 > results/exp_scale_arxiv-full_seed0.md   # circa 45 minuti; lo stesso con msmarco
uv run bench_scale.py arxiv-full > results/bench_scale_arxiv-full.md        # circa 2 ore, a macchina libera
uv run check_split.py arxiv-full > results/check_split_arxiv-full.md
```

Gli embedding finiscono in `data/`, che non è sotto controllo di versione: ogni file pesa da 300 a 650 MB, quelli a scala grande 2,4 GB.

## Dati e modelli

- Notizie: [`heegyu/news-category-dataset`](https://huggingface.co/datasets/heegyu/news-category-dataset), titoli e sommari di HuffPost, 2012-2022.
- Abstract: [`gfissore/arxiv-abstracts-2021`](https://huggingface.co/datasets/gfissore/arxiv-abstracts-2021), 210.000 articoli estratti a caso tra il 2007 e il 2021.
- Scala grande: tutti gli abstract dello stesso dataset arXiv (1.585.373) e 1.600.000 passaggi estratti a caso da [`BeIR/msmarco`](https://huggingface.co/datasets/BeIR/msmarco), con 3.000 delle sue domande.
- Embedding: [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) e [`bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5).

Le revisioni di dataset e modelli non sono fissate: scaricandoli in futuro i numeri possono cambiare leggermente.

## Limiti da tenere presenti

- Indici da 200.000 a 1.550.000 vettori su un portatile. A scale molto più grandi il costo del ricalcolo completo cresce e le conclusioni pratiche possono cambiare.
- Le interrogazioni sono testi del corpus tenuti fuori dall'indice; domande vere di utenti solo su MS MARCO, che però non ha date e quindi non ha deriva.
- DeDrift è riscritto dal testo del paper, perché non risulta codice pubblicato; Ada-IVF e SPFresh non sono stati provati.
- Faiss 1.16.0. Il ramo principale di Faiss ha poi cambiato la rianimazione dei cluster: lì sono stati rifatti l'aggiornamento singolo e una corsa a scala grande (`results/*_main.md`, `results/check_main_revival_*.md`), con Faiss compilato dai sorgenti al commit 16a95d6.

## Licenza

Codice e testi sotto licenza MIT (`LICENSE`). Dataset e modelli hanno le licenze dei rispettivi autori.
