#!/bin/bash
# Night queue, second part: one job at a time. Every output goes to a temporary file
# and replaces the previous one only if the job succeeds. Timings are measured on an idle machine.
cd "$(dirname "$0")"
failures=0
job() {  # job <label> <output file> <command...>
  local label="$1" out="$2"; shift 2
  echo "$(date '+%H:%M:%S') start $label" >> data/night.log
  if "$@" > "$out.tmp" 2> "data/night_$label.err"; then
    mv "$out.tmp" "$out"; echo "$(date '+%H:%M:%S') end $label" >> data/night.log
  else
    failures=$((failures + 1)); echo "$(date '+%H:%M:%S') FAILED $label (see data/night_$label.err)" >> data/night.log
  fi
}
exps() { for c in "$@"; do job "exp-$c" "results/exp_real_$c.md" uv run exp_real.py "$c"; done; }
checks() { for c in "$@"; do job "check-$c" "results/check_recall_$c.md" uv run check_recall_vs_faiss.py "$c"; done; }
benches() { for c in "$@"; do sleep 60; job "bench-$c" "results/bench_rebuild_$c.md" uv run bench_rebuild.py "$c"; done; }
exps news arxiv news-bge
checks news arxiv news-bge
benches news arxiv news-bge
echo "$(date '+%H:%M:%S') FIRST PART FINISHED, failed jobs: $failures" >> data/night.log
job embed-arxiv-bge data/embed_arxiv-bge.log uv run --group real embed_corpus.py arxiv bge
exps arxiv-bge; checks arxiv-bge; benches arxiv-bge
echo "$(date '+%H:%M:%S') QUEUE FINISHED, failed jobs: $failures" >> data/night.log
