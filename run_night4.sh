#!/bin/bash
# Coda notturna a scala grande: un lavoro alla volta. Ogni uscita va in un file provvisorio
# e sostituisce quella precedente solo se il lavoro riesce. I tempi (bench) si misurano a macchina libera.
cd "$(dirname "$0")"
failures=0
job() {  # job <etichetta> <file di uscita> <comando...>
  local label="$1" out="$2"; shift 2
  echo "$(date '+%H:%M:%S') inizio $label" >> data/night4.log
  if "$@" > "$out.tmp" 2> "data/night4_$label.err"; then
    mv "$out.tmp" "$out"; echo "$(date '+%H:%M:%S') fine $label" >> data/night4.log
  else
    failures=$((failures + 1)); echo "$(date '+%H:%M:%S') FALLITO $label (vedi data/night4_$label.err)" >> data/night4.log
  fi
}
job embed-msmarco data/embed_msmarco.log uv run --group real embed_corpus.py msmarco
sleep 120
job bench-arxiv-full results/bench_scale_arxiv-full.md uv run bench_scale.py arxiv-full
job main-arxiv-full results/exp_scale_arxiv-full_seed0_main.md vendor/faiss_venv/bin/python exp_scale.py arxiv-full 0
job split-arxiv-full results/check_split_arxiv-full.md uv run check_split.py arxiv-full 0
job exp-msmarco results/exp_scale_msmarco_seed0.md uv run exp_scale.py msmarco 0
job bench-msmarco results/bench_scale_msmarco.md uv run bench_scale.py msmarco
echo "$(date '+%H:%M:%S') CODA FINITA, lavori falliti: $failures" >> data/night4.log
