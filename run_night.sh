#!/bin/bash
# Coda notturna: un lavoro alla volta, mai due insieme, così tempi e risultati non si sporcano.
# I banchi dei tempi sono gli ultimi e girano a macchina libera.
cd "$(dirname "$0")"
job() {  # job <etichetta> <file di uscita> <comando...>
  local label="$1" out="$2"; shift 2
  echo "$(date '+%H:%M:%S') inizio $label" >> data/night.log
  "$@" > "$out" 2> "data/night_$label.err"
  echo "$(date '+%H:%M:%S') fine $label (uscita $?)" >> data/night.log
}
job embed-news-bge data/embed_news-bge.log uv run --group real embed_corpus.py news bge
job embed-arxiv-bge data/embed_arxiv-bge.log uv run --group real embed_corpus.py arxiv bge
for c in news arxiv news-bge arxiv-bge; do job "exp-$c" "results/exp_real_$c.md" uv run exp_real.py "$c"; done
for c in news arxiv news-bge arxiv-bge; do job "check-$c" "results/check_recall_$c.md" uv run check_recall_vs_faiss.py "$c"; done
sleep 60
for c in news arxiv news-bge arxiv-bge; do job "bench-$c" "results/bench_rebuild_$c.md" uv run bench_rebuild.py "$c"; sleep 30; done
echo "$(date '+%H:%M:%S') CODA FINITA" >> data/night.log
