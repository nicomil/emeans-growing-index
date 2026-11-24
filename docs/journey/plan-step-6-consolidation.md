---
title: 'Plan for step 6: consolidate and write'
status: draft
created: 2026-11-22
---

# Plan for step 6: consolidate and write

## Where we are

Five experimental steps closed, each with a spec and a review. The question in the brief was how much to trust the old centroids as a function of the drift. The answer found is different from the one sought.

Four results hold up, on synthetic data and on real embeddings:

1. e-means rebuilds an index in a fraction of the time of classic k-means, on a laptop and on real text too: 5 times faster at equal error, recall within half a point of the reference with 3 epochs.
2. Using e-means incrementally in the most obvious way (old centroids as the start, new data only) destroys the index: recall from 0.83 to 0.05.
3. Without re-reading the vectors already inserted, no variant of e-means does better than classic mini-batch k-means. About 40% of the lost recall is recovered.
4. On 200,000 articles and four and a half years, not refreshing costs 6 points of recall, 11 on recent queries; 5 of the 6 are drift.

Two things did not hold up: a law that chooses the initial mass from the drift, and the advantage of the warm start in search.

The brief has not been updated: it still describes the initial hypothesis. It has to be realigned before writing (activity 6.0).

## Goal of the step

Turn the results into a publishable study, after closing the three points that an expert reader would challenge first.

## Activities, in order

Each activity has an exit criterion. If a criterion fails, the plan says what changes.

### 6.0 Realign the brief — done, approved on 23 November 2026 with a hybrid thread

Rewrite the summary, solution and success criteria of the brief on the basis of the results. The abandoned hypotheses stay in the decision log.

- Done when: the brief describes the study we will write, and you recognise it as yours.

### 6.1 Check the warning with the Faiss code — done, confirmed (see `recent-literature.md`)

Result 2 is the most useful to the reader and was measured with `emeans.py`, our rewrite. It has to be repeated by calling Faiss's `NumpyEmeans.train(nuovi, init_centroids=vecchi)` directly on the real embeddings.

- Done when: the recall with the Faiss code is reported next to ours.
- If Faiss does not show the collapse: result 2 becomes "an implementation faithful to the paper's algorithm shows it, the shipped one does not", and the reason has to be understood before writing a single line.

### 6.2 Check the recent literature — done, topic not covered (see `recent-literature.md`)

Look for works that came out after 6 November 2026 on e-means in incremental, warm or drift scenarios, and the discussions in the Faiss repository. Re-read how DeDrift, Ada-IVF and SPFresh measure drift, in order to use the same terms.

- Done when: there is a list of works with one line each on what they cover and what they do not.
- If someone has already published the same results: the study is presented as an independent replication on text and on a laptop, not as something new.

### 6.3 Second corpus — done (see `spec-6-consolidation.md`)

The whole result on real data rests on HuffPost: short texts, a single domain. Repeat `exp_real.py` on arXiv abstracts (`gfissore/arxiv-abstracts-2021`, the date is derived from the identifier): longer texts, close to the document chunks of a RAG system, and strong topic drift.

- Work: make `embed_news.py` and `exp_real.py` independent of the corpus; extract about 300,000 abstracts in date order; re-run.
- Done when: the table of step 5 exists for both corpora.
- If a result does not repeat: it is reported as such, with the corpus on which it holds.

### 6.4 Strengthening the measurement — done, with a second embedding model on top

Only those that touch the four main results:

- confidence interval over the queries (resampling), to say which differences in recall are real;
- recall at two cost levels, 0.1% and 1% of the index, as in Appendix L of the paper;
- timings repeated three times in alternating order, with the recall next to them.

- Done when: every number cited in the text has its interval.

Out of the plan, on purpose: per-cluster mass, local reassignment, scaling law, direct comparison with DeDrift or SPFresh, Italian corpus. They are to be cited as future work.

### 6.5 Write — the drafts of the post and of the documentation request are done; the long article remains to be written

Proposed structure:

0. Context preamble, for those who do not work with these indexes: what a RAG system is and where the vector index sits; the two ways of building it, graph-based (HNSW) and cluster-based (IVF); strengths and limits of each and at what scale one or the other is used; where this study sits (cluster-based indexes only) and what changes for those who use HNSW.
1. What e-means promises and what we wanted to check.
2. Replication on real text and on a laptop: timings, error, recall.
3. What it costs not to refresh an index: the drift measured.
4. "I already have good centroids, can I reuse them?" First way, the most obvious: train e-means on the new documents only. Why it breaks the index (zero initial mass, cluster revival).
5. Second way: give the old centroids a weight. Reduced mass, rule from the signal, and the measurement error that had made us believe in an advantage.
6. Third way: reuse them while re-reading everything. What changes in the error and what does not in search.
7. What to do in practice: rebuild, with how many epochs, how often.
8. Limits and future work.

Figures: time against error for the two algorithms; recall over time by strategy; the 2D animation as an illustration of the mechanism; recall before and after the naive use.

Sections 4-6 follow the thread of the warm start; section 5 is the point that sets the study apart from a summary of the paper: it also tells the conclusions withdrawn after review.

- Done when: there is a complete draft and a README that makes it possible to redo every table with one command.

### 6.6 Final review — done on the two short texts, two passes

Review of the text with `bmad-review` (structure and prose) and a check that every number in the text matches the files in `results/`.

- Done when: no number in the text lacks a source in the repository.

## Decisions taken (22 November 2026)

1. **Language and venue:** Italian at first; the repository was later translated to English.
2. **Repository:** public, but later on.
3. **Abandoned paths:** a section in the body of the text, not an appendix.
4. **Second corpus:** arXiv abstracts.

## Estimate

About three days of work: half a day for 6.0-6.2, one for 6.3-6.4, one and a half for 6.5-6.6. Activities 6.1 and 6.2 have to be done first because they can change what gets written.

## Risks

- 6.1 may show that the collapse depends on a detail of our rewrite. It is the most serious risk, which is why it is the first activity.
- 6.2 may take away novelty. The study remains useful as a replication.
- 6.3 may give different results on long texts. It has to be reported, not hidden.
