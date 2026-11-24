#!/bin/bash
# Night queue: Stack Overflow, real drift and real user questions together. One job at a time.
# Every output goes to a temporary file and replaces the previous one only if the job succeeds.
cd "$(dirname "$0")"
failures=0
job() {  # job <label> <output file> <command...>
  local label="$1" out="$2"; shift 2
  echo "$(date '+%H:%M:%S') start $label" >> data/night5.log
  if "$@" > "$out.tmp" 2> "data/night5_$label.err"; then
    mv "$out.tmp" "$out"; echo "$(date '+%H:%M:%S') end $label" >> data/night5.log
  else
    failures=$((failures + 1)); echo "$(date '+%H:%M:%S') FAILED $label (see data/night5_$label.err)" >> data/night5.log
  fi
}
job embed-stackoverflow data/embed_stackoverflow.log uv run --group real embed_corpus.py stackoverflow
for seed in 0 1 2; do
  job exp-stackoverflow-$seed results/exp_scale_stackoverflow_seed$seed.md uv run exp_scale.py stackoverflow $seed
done
echo "$(date '+%H:%M:%S') QUEUE FINISHED, failed jobs: $failures" >> data/night5.log
