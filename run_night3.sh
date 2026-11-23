#!/bin/bash
# Coda notturna, seconda parte: un lavoro alla volta. Ogni uscita va in un file provvisorio
# e sostituisce quella precedente solo se il lavoro riesce. I tempi si misurano a macchina libera.
cd "$(dirname "$0")"
failures=0
job() {  # job <etichetta> <file di uscita> <comando...>
  local label="$1" out="$2"; shift 2
  echo "$(date '+%H:%M:%S') inizio $label" >> data/night.log
  if "$@" > "$out.tmp" 2> "data/night_$label.err"; then
    mv "$out.tmp" "$out"; echo "$(date '+%H:%M:%S') fine $label" >> data/night.log
  else
    failures=$((failures + 1)); echo "$(date '+%H:%M:%S') FALLITO $label (vedi data/night_$label.err)" >> data/night.log
  fi
}
exps() { for c in "$@"; do job "exp-$c" "results/exp_real_$c.md" uv run exp_real.py "$c"; done; }
checks() { for c in "$@"; do job "check-$c" "results/check_recall_$c.md" uv run check_recall_vs_faiss.py "$c"; done; }
benches() { for c in "$@"; do sleep 60; job "bench-$c" "results/bench_rebuild_$c.md" uv run bench_rebuild.py "$c"; done; }
exps arxiv-bge; checks arxiv-bge; benches arxiv-bge
echo "$(date '+%H:%M:%S') CODA FINITA, lavori falliti: $failures" >> data/night.log
