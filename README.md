# e-means and indexes that change: update or rebuild?

An independent study of [e-means](https://arxiv.org/abs/2611.09501), the k-means variant published by Meta FAIR in November 2026 and shipped in Faiss 1.16.0, in a situation the paper does not cover: a cluster-based vector index (IVF) that receives new documents over time.

The full tables, with confidence intervals, are in `results/SUMMARY.md`. A beginner-friendly explanation is in `docs/study.html`. The project brief (`brief.md`) and the step-by-step journey, with the reviews, are in `docs/journey/`.

## Results in brief

An IVF index of 800,000 vectors receives ten batches of 75,000 new ones (1.55 million at the end, 16,384 centroids). Recall@10 against exact search, scanning 1% of the vectors per query, Faiss 1.16.0, on a MacBook Air M1 with 16 GB:

| After ten refreshes | arXiv abstracts, date order | MS MARCO passages, real Bing queries |
|---|---:|---:|
| Never retrain the centroids, only add the new vectors | 0.989 | 0.928 |
| Retrain with e-means on the new vectors only, starting from the old centroids; old vectors left in their lists | 0.085 | 0.080 |
| Same centroids, all vectors reassigned | 0.944 | 0.830 |
| Full rebuild on all vectors, e-means, 3 epochs | 0.992 | 0.932 |

arXiv is the mean of three seeds (spread at most 0.007); MS MARCO is one seed and has no dates, so no drift.

- **The naive refresh breaks the index silently.** `NumpyEmeans(d, k, nepochs=1).train(new_vectors, init_centroids=old_centroids)` raises no error and no warning. The starting centroids carry almost no weight (the paper says so in §3.1), so the result describes the new batch only.
- **A full rebuild is cheap.** Three e-means epochs plus reassigning all 1.55 million vectors take about 4 minutes on the laptop.
- **Doing nothing holds up well** at this operating point: 0.3 points below the 3-epoch rebuild on arXiv scanning 1%, 3.1 points scanning 0.1% (0.867 against 0.898).
- **The speed advantage of e-means over k-means depends on the dataset.** On arXiv, 3 epochs (178 s) match the recall of 10 to 25 k-means iterations (553 to 1,382 s); on MS MARCO, 5 k-means iterations (277 s) are enough to match them.
- **On the Faiss main branch** (commit 16a95d6, one seed) the naive refresh still collapses: 0.067 with the lists left as they are, 0.953 with all vectors reassigned.

The same pattern holds at 200,000 vectors on four datasets (HuffPost news and arXiv, two embedding models); see `results/SUMMARY.md`.

## What is here

| File | What it does |
|---|---|
| `emeans.py` | e-means in one short NumPy file, with what Faiss does not expose: initial mass of the centroids and final averages that can be switched off |
| `test_emeans.py` | Tests, including the comparison with the Faiss implementation |
| `demo_2d.py` | Animation of the centroids on points in two dimensions |
| `exp_warm.py`, `exp_new_only.py`, `exp_rule.py`, `exp_sequence.py` | Experiments on synthetic data with controlled drift (steps 3, 4, 4b, D) |
| `embed_corpus.py` | Downloads a dated corpus and computes its embeddings |
| `exp_real.py` | Index update strategies on real embeddings: error and recall |
| `bench_rebuild.py` | Timings of the full rebuild, e-means against classic k-means |
| `check_recall_vs_faiss.py` | Checks that the recall computed here matches that of a Faiss IVF index |
| `check_faiss_naive.py` | The naive refresh and its fix, done with the Faiss code |
| `check_naive_baselines.py` | The same refresh with k-means and with two update sizes |
| `check_main_revival.py` | On the Faiss main branch: how much it depends on cluster revival |
| `exp_scale.py` | The experiment at 1.5 million texts and 16,384 centroids, with Faiss code only and the comparison with DeDrift |
| `bench_scale.py` | Timings of the full rebuild at that scale |
| `check_split.py` | How much the choices that the DeDrift paper leaves open matter |
| `analyze.py` | Summary with confidence intervals |
| `docs/repro_emeans_init_centroids.py` | Minimal, self-contained reproduction of the behaviour of `init_centroids` |

## Reproducing the results

You need [uv](https://docs.astral.sh/uv/). Dependencies install themselves on the first command.

```bash
uv run pytest -q                                   # tests, a few seconds

# synthetic data
uv run exp_warm.py                                 # about 1 minute
uv run exp_new_only.py overlapping                 # also: separated, no-drift; 3-4 minutes each
uv run exp_rule.py overlapping > results/exp_rule_overlapping.md
uv run exp_rule.py separated > results/exp_rule_separated.md
uv run exp_sequence.py > results/exp_sequence.md   # requires the previous command

# real data: embeddings first, once per dataset
uv run --group real embed_corpus.py news           # news, 384-dimension model: a few minutes
uv run --group real embed_corpus.py arxiv          # abstracts, downloads 1.4 GB: about 15 minutes
uv run --group real embed_corpus.py news bge       # 768-dimension model: about 30 minutes
uv run --group real embed_corpus.py arxiv bge      # a few hours on a laptop

# then, for each dataset (news, arxiv, news-bge, arxiv-bge)
uv run exp_real.py news > results/exp_real_news.md                  # about 30 minutes
uv run check_recall_vs_faiss.py news > results/check_recall_news.md
uv run bench_rebuild.py news > results/bench_rebuild_news.md        # on its own, on an idle machine
uv run check_faiss_naive.py news > results/check_faiss_naive_news.md
uv run check_naive_baselines.py news > results/check_naive_baselines_news.md
uv run analyze.py > results/SUMMARY.md
```

`run_night2.sh` runs the real-data part in a row, one job at a time.

To repeat the single update on the Faiss main branch you need to build it (CMake, SWIG, libomp) and use that Python instead of `uv run`:

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

Large scale (1.5 million texts; it takes about 2 hours of embedding for arXiv, 1 for MS MARCO, and 16 GB of memory):

```
uv run --group real embed_corpus.py arxiv-full
uv run --group real embed_corpus.py msmarco
uv run exp_scale.py arxiv-full 0 > results/exp_scale_arxiv-full_seed0.md   # about 45 minutes; the same with msmarco
uv run bench_scale.py arxiv-full > results/bench_scale_arxiv-full.md        # about 2 hours, on an idle machine
uv run check_split.py arxiv-full > results/check_split_arxiv-full.md
```

The embeddings end up in `data/`, which is not under version control: each file weighs 300 to 650 MB, the large-scale ones 2.4 GB.

## Data and models

- News: [`heegyu/news-category-dataset`](https://huggingface.co/datasets/heegyu/news-category-dataset), HuffPost headlines and summaries, 2012-2022.
- Abstracts: [`gfissore/arxiv-abstracts-2021`](https://huggingface.co/datasets/gfissore/arxiv-abstracts-2021), 210,000 papers sampled at random between 2007 and 2021.
- Large scale: all the abstracts of the same arXiv dataset (1,585,373) and 1,600,000 passages sampled at random from [`BeIR/msmarco`](https://huggingface.co/datasets/BeIR/msmarco), with 3,000 of its queries.
- Embeddings: [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) and [`bge-base-en-v1.5`](https://huggingface.co/BAAI/bge-base-en-v1.5).

The revisions of datasets and models are not pinned: downloading them in the future may change the numbers slightly.

## Limits to keep in mind

- Indexes from 200,000 to 1,550,000 vectors on a laptop. At much larger scales the cost of the full rebuild grows and the practical conclusions may change.
- The queries are texts from the corpus held out of the index; real user questions only on MS MARCO, which however has no dates and therefore no drift.
- DeDrift is rewritten from the text of the paper, because no published code appears to exist; Ada-IVF and SPFresh were not tried.
- Faiss 1.16.0. The Faiss main branch has since changed cluster revival: the single update and one large-scale run were redone there (`results/*_main.md`, `results/check_main_revival_*.md`), with Faiss built from source at commit 16a95d6.

## Licence

Code and texts under the MIT licence (`LICENSE`). Datasets and models carry the licences of their respective authors.
