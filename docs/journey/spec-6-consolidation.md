---
title: 'Step 6: consolidation of the results and drafts for publication'
type: 'feature'
created: '2026-11-23'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/journey/plan-step-6-consolidation.md'
  - '{project-root}/docs/journey/brief.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The results of step 5 rested on one corpus, one embedding model, three seeds without intervals and timings measured once. The goal is a small post on LinkedIn and then a documentation request in the Faiss repository: accurate data and valid experiments are needed before getting there.

**Approach:** In one night of work with no overlap between the computations: second corpus, second embedding model, confidence intervals, clean timings, check of the measurement against Faiss, demonstration of the cause with the Faiss code, and the drafts of the two texts. No text is published: sending is the user's decision.

</frozen-after-approval>

## Implementation Notes

**What was run**

Jobs in a queue, one at a time, logged in `data/night.log`: embeddings, experiment on each dataset, recall check, timings last on an idle machine. Zero failed jobs in the first part.

| Plan activity | Outcome |
|---|---|
| 6.0 Brief | approved on 23 November, hybrid thread |
| 6.1 Warning checked with the Faiss code | confirmed; in addition, the fix made with the Faiss code restores recall |
| 6.2 Recent literature | topic not covered; found active work on cluster revival in the Faiss repository (#5907, #5915) |
| 6.3 Second corpus | arXiv, results in agreement, weaker drift |
| 6.4 Strengthening the measurement | intervals, two cost levels, repeated timings, second embedding model, check against IndexIVFFlat |
| 6.5 Writing | draft of the post and of the documentation request; the long article was not written |
| 6.6 Final review | done on the three short documents |

**New or rewritten files**

`exp_real.py`, `bench_rebuild.py`, `check_recall_vs_faiss.py`, `check_faiss_naive.py`, `analyze.py`, `embed_corpus.py`, `run_night2.sh`, `README.md`, `docs/REPORT.md` (since folded into the README), `docs/linkedin-post-bozza.md`, `docs/faiss-issue-bozza.md`, `docs/repro_emeans_init_centroids.py`, `results/SUMMARY.md` and the results files per dataset.

**Results**

They are in `results/SUMMARY.md`; the reasoned summary is in `docs/REPORT.md` (since folded into the README). In short, on three datasets:

- the naive use of e-means (old centroids as the start, training on the new texts only) lowers recall by 30-58% after a single update of 10,000 texts even when the lists are rebuilt, as much as a start from random rows; k-means used the same way loses 5-24%; with 50,000 new texts e-means loses 4-15%;
- the causes are the almost zero weight of the starting centroids and the final means computed on the new texts only; with both fixed using the Faiss code, recall returns to the level of classic mini-batch k-means;
- the full rebuild with e-means at three epochs gets to 0.2-0.7 points of recall from the reference in 4-7 seconds;
- e-means is more than 4-5 times faster than k-means at equal error, 2.5-4 times at equal recall with 0.1% of the index read, and is not faster at equal recall with 1% read.

**Two earlier claims corrected by this step**

- "e-means is 5 times faster" held for the error, not for recall in general.
- "recall collapses from 0.83 to 0.05" held with the lists left as they are; with the lists rebuilt, which is the realistic case, it drops to 0.42 after one update.

**Surprises**

- With the 768-dimension model the warm start with steady-state mass gives half a point of recall more than starting from scratch, a small difference but consistent across the seeds; with the 384-dimension model it gives nothing.
- A timings file left over from a reduced-scale trial was about to end up in the summary: the review noticed it. Now every output is written to a temporary file and replaces the previous one only if the job succeeds.

**Not done**

- The test on the Faiss main branch was not done during the night: the system denied execution of the freshly downloaded sources and the block was not worked around. It was done on the morning of 23 November with the user's authorization, building Faiss at commit 16a95d6: the damage of the naive use remains (from 16% to 47% less recall) and, with the new cluster revival, initial mass and moving average are no longer enough to remove it.
- arXiv with the second embedding model had not finished by the morning: a restart of the machine interrupted the queue. Resumed and completed at 10:35 on 23 November; results in agreement with the other three datasets, summarised in `docs/REPORT.md` (since folded into the README).
- The long article foreseen by the plan.

## Review Triage Log

Three reviews in this step. The findings are many: here are the outcomes by group; the detail is in the commit messages of `5d3dd4a` and later.

| Review | Findings | Fixed | Outcome of the main ones |
|---|---|---|---|
| Night code (Blind Hunter) | 16 | 13 | Random reading inside the partial lists; saving per seed; two units of "mass" named; warm start without final means added; timing repetitions balanced with load recorded; comparison at equal error as a bracket and not by interpolation; test of the recall against an obvious version; row with k-means in the reproduction. Rejected: lock against a second instance of the queue, correction for multiple comparisons (stated in the limits), pinned revisions of dataset and models (stated in the limits). |
| Draft of the documentation request, read as a maintainer | about 30 | almost all | Rewritten as a request for documentation; acknowledged what the code already documents; cause shown with the Faiss code; rebuilt lists in the foreground; percentages corrected (from 30% to 58%); unit of the mass specified; stated that the fix is of little use in practice. Not done: test on the main branch. |
| Final documents, number by number | about 45 | almost all | No invented numbers, but: numbers for the news presented as general, training timings called "index rebuild", time ratios at equal recall based on differences of a few thousandths, and above all no generic comparison on the real data. Added `check_naive_baselines.py`: k-means used the same way loses from 5% to 24%, e-means from 30% to 58% and as much as a start from random rows; with updates of 50,000 texts the damage drops to 4-15%. Post, documentation request and report rewritten accordingly. Reviewer's verdict on the documentation request before the fixes: not ready. After: the test on the Faiss main branch remains open. |
