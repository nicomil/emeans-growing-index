#!/bin/bash
# Night queue at large scale: one job at a time. Every output goes to a temporary file
# and replaces the previous one only if the job succeeds. Timings (bench) are measured on an idle machine.
cd "$(dirname "$0")"
failures=0
job() {  # job <label> <output file> <command...>
  local label="$1" out="$2"; shift 2
  echo "$(date '+%H:%M:%S') start $label" >> data/night4.log
  if "$@" > "$out.tmp" 2> "data/night4_$label.err"; then
    mv "$out.tmp" "$out"; echo "$(date '+%H:%M:%S') end $label" >> data/night4.log
  else
    failures=$((failures + 1)); echo "$(date '+%H:%M:%S') FAILED $label (see data/night4_$label.err)" >> data/night4.log
  fi
}
job embed-msmarco data/embed_msmarco.log uv run --group real embed_corpus.py msmarco
sleep 120
job bench-arxiv-full results/bench_scale_arxiv-full.md uv run bench_scale.py arxiv-full
job main-arxiv-full results/exp_scale_arxiv-full_seed0_main.md vendor/faiss_venv/bin/python exp_scale.py arxiv-full 0
job split-arxiv-full results/check_split_arxiv-full.md uv run check_split.py arxiv-full 0
job exp-msmarco results/exp_scale_msmarco_seed0.md uv run exp_scale.py msmarco 0
job bench-msmarco results/bench_scale_msmarco.md uv run bench_scale.py msmarco
echo "$(date '+%H:%M:%S') QUEUE FINISHED, failed jobs: $failures" >> data/night4.log
