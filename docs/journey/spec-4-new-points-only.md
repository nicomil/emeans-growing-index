---
title: 'Step 4: updating the centroids by reading only the new points'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/journey/brief.md'
  - '{project-root}/docs/journey/spec-3-warm-start.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** In step 3 all the strategies reread the whole data set, and there the initial mass mattered little. The real use case is a different one: one does not want to reread the old data, and the centroids are updated with the new points only, at a cost proportional to how many there are. In that case nothing has been measured.

**Approach:** An experiment in which e-means starts from the old centroids and reads the new points only, once, with a grid over initial mass, step size and revival threshold. The error is measured on all the data, separated between old and new points, and is compared with the exact incremental mean and with the strategies that reread everything. It covers data without well-separated groups and data with well-separated groups.

</frozen-after-approval>

## Implementation Notes

**Code**

- `exp_new_only.py`: the experiment. `uv run exp_new_only.py overlapping`, `separated` or `no-drift`, three to four minutes each. Raw numbers in `results/exp_new_only_<type>.json`, full tables in `results/exp_new_only_<type>.md`.
- `exp_warm.py`: `mixture` has one more parameter, the spread of the means.
- `test_emeans.py`: one new test on the link between e-means and classic mini-batch k-means.
- `emeans.py` has not changed.

**Units of the knobs**

- Mass m: initial mass = m × initial step size × number of old points in the cluster. At a constant and very small step size, m = 1 makes e-means equal to the classic mini-batch k-means that starts from the true counts: an old point weighs as much as a new one (there is a test for this). With the cosine step size of e-means the new points weigh from 1 to 0.1 times an old point along the pass, 0.55 on average: m = 1 retains the past about 1.8 times more than equal weighting would.
- Step size s: initial step size = s × the one from the scaling law computed on the number of new points.
- Threshold tau: 0.1 as in the paper, or 0 (cluster revival off).

**Design**

- 50,000 old points at 32 dimensions, 256 centroids, new points at 5%, 20% and 50% of the total. Three types of data: new points from a shifted zone with overlapping components; the same with well-separated groups; new points from the same distribution as the old ones (no drift).
- Of the old data only the centroids and the number of points per cluster are used, which an IVF index knows. In the experiment the counts come from a reassignment of the old data; the centroids come out of the e-means finalization and are not exactly the means of the points counted.
- 5 data sets × 2 seeds of the algorithm. The 10 runs are not independent: the old centroids and the strategies without randomness change only with the data set.
- Reference: e-means from scratch on all the data, 10 epochs. Each excess is computed against the reference of the same run.
- Equal-cost comparisons: Lloyd on the new points with the old statistics frozen; classic mini-batch k-means that starts from the true counts, with the same batches as e-means.
- e-means: one fixed configuration for all the columns and all the data types (m 0.3, s 1/4, no cluster revival), chosen at the centre of the grid after the first run and not retouched; plus the grid m in {0.03; 0.1; 0.3; 1; 3}, s in {1/64; 1/16; 1/4; 1}, tau in {0.1; 0}. Always without finalization.

**Results with drift, data without well-separated groups**

Excess error on all the data, median [minimum; maximum]. The second column is the share of data read.

| Strategy | Reads | 5% new | 20% new | 50% new |
|---|---|---|---|---|
| old centroids, no recomputation | 0 | +2.35% [2.15; 2.50] | +12.65% [12.06; 12.84] | +31.48% [29.81; 32.71] |
| e-means, almost zero mass and finalization | f | +66.40% [63.48; 68.35] | +54.78% [51.79; 58.12] | +31.54% [29.25; 33.20] |
| Lloyd with old statistics frozen | f | +1.69% [1.48; 1.90] | +7.09% [6.77; 7.54] | +12.62% [11.79; 13.55] |
| mini-batch k-means with true counts | f | +1.29% [1.14; 1.45] | +6.37% [5.70; 6.56] | +9.01% [7.85; 10.16] |
| e-means, fixed configuration | f | +1.27% [1.07; 1.37] | +4.89% [4.41; 5.37] | +3.25% [2.53; 4.53] |
| frozen Lloyd, 3 passes | 3f | +1.27% [1.08; 1.42] | +5.46% [5.26; 5.84] | +6.32% [5.08; 7.10] |
| e-means, fixed configuration, 3 epochs | 3f | +1.65% [1.36; 1.91] | +4.41% [3.54; 5.09] | +7.27% [6.03; 8.21] |
| warm on all the data, 1 epoch | 1 | +1.36% [1.22; 1.64] | +1.98% [1.71; 2.27] | +0.25% [−0.15; 0.74] |

Grid with cluster revival off, median excess; in parentheses, in how many runs out of 10 it beats the mini-batch k-means with true counts.

| m | 5%: s 1/64 | 1/4 | 1 | 20%: s 1/64 | 1/4 | 1 | 50%: s 1/64 | 1/4 | 1 |
|---|---|---|---|---|---|---|---|---|---|
| 0.03 | +2.67 (0) | +2.94 (0) | +4.39 (0) | +5.21 (10) | +5.52 (10) | +10.99 (0) | +4.00 (10) | +5.70 (10) | +15.66 (0) |
| 0.1 | +1.48 (0) | +1.59 (0) | +2.29 (0) | +4.54 (10) | +4.23 (10) | +6.80 (0) | +3.17 (10) | +2.77 (10) | +13.77 (0) |
| 0.3 | +1.27 (9) | +1.27 (9) | +1.39 (1) | +5.46 (10) | +4.89 (10) | +4.60 (10) | +5.91 (10) | +3.25 (10) | +11.56 (0) |
| 1 | +1.43 (0) | +1.35 (0) | +1.24 (10) | +7.03 (0) | +6.45 (0) | +4.37 (10) | +11.13 (0) | +7.05 (10) | +8.40 (8) |
| 3 | +2.02 (0) | +1.91 (0) | +1.45 (0) | +8.02 (0) | +7.63 (0) | +5.22 (10) | +15.85 (0) | +12.04 (0) | +5.37 (10) |

With cluster revival on, the cells are the same at 5%; at 20% and 50% they get worse where the step size is large, by up to +30 points. None improves.

**Results without drift**

| Strategy | Reads | 5% new | 20% new | 50% new |
|---|---|---|---|---|
| old centroids, no recomputation | 0 | +0.14% | +0.28% | +0.49% |
| e-means, almost zero mass and finalization | f | +17.86% | +7.54% | +1.08% |
| mini-batch k-means with true counts | f | +0.11% | +0.16% | +0.17% |
| e-means, fixed configuration | f | +0.16% | +0.29% | +0.27% |
| e-means, best cell of the grid | f | +0.12% | +0.17% | +0.17% |

No cell of the grid beats the mini-batch k-means with true counts, in any run. The best cells have m between 1 and 3; with m below 0.3 the error rises. The fixed configuration with 5% and 20% of new points does no better than leaving the old centroids.

**What holds**

1. **The naive use always does harm.** Passing the old centroids to e-means and training it on the new points only with the default almost zero mass raises the error in all the cases tried, even without drift (+17.86% with 5% of new points) and even compared with doing nothing. With drift the error on the old points rises by 63-75%.
2. **Without drift e-means is not needed.** The classic mini-batch k-means with the true counts is the best and is enough.
3. **With drift, giving less weight to the past helps, and here e-means with reduced mass beats the equal-cost comparisons.** With 20% and 50% of new points the fixed configuration scores +4.89% and +3.25% against +6.37% and +9.01% for the classic mini-batch, with disjoint ranges. With 5% they are level. The advantage does not come from the algorithm in itself: it comes from being able to forget, which lets the centroids migrate towards the new zone.
4. **The best mass depends on how much drift there is.** Without drift m between 1 and 3; with drift and 5% of new points about 0.3; with 20% and 50% about 0.1. It is the answer, in direction, to the question of the brief. It is not a formula: the grid proceeds in jumps of a factor of 3 and there is a single type of drift.
5. **Mass and step size compensate each other.** A larger step size forgets faster and tolerates a higher mass.
6. **The cluster revival of e-means is unsuited to this scenario.** It discounts the mass of all the clusters at every step, even of those that receive no points. An old cluster without new points ends up below threshold and is recycled although its points still exist. Off, it never makes things worse; on, it costs up to 30 points.
7. **More passes over the new points only do not help e-means**: with three epochs it forgets more (at 50%, error on the old points +13%). They do help the frozen Lloyd, which with three passes reaches the fixed configuration at 5% but not at 20% and 50%.
8. **Rereading everything remains better when the new points are many**: one warm epoch on all the data gives +1.98% and +0.25% against +4.89% and +3.25%. With 5% of new points there is no difference, at one twentieth of the reads.

**On data with well-separated groups**

The reference is unstable (it is beaten by up to 20% by strategies it should bound) and the absolute values cannot be used. The paired comparisons go in the same direction: the naive use brings the error to +438%, +371%, +177%; the fixed configuration beats the classic mini-batch in 9-10 runs out of 10; the best mass decreases with the new points down to 0.03 with 50%, which is the edge of the grid. With 50%, three passes of frozen Lloyd do better than the fixed configuration with one pass.

**The open point**

The right mass depends on the drift, which in practice is not known in advance. The data suggest a signal measurable without rereading the old ones: the error of the new points on the old centroids, compared with the typical one of the old points. Without drift it is +1-2%; with drift +45-72%. Choosing the mass from that signal is the natural next step.

**Limits**

- A single combination of n, k and dimension; a single type of drift (shifted zone, all the new points from the new zone). The mixed cases are missing.
- The grid does not bracket the minimum at several points: s = 1 with 5% of new points, m = 0.03 with 50% on the well-separated groups.
- The fixed configuration was chosen after seeing the first grid, on the same data.
- The cells of the grid report only median and number of wins; differences of a few hundredths of a point cannot be distinguished.
- Error on the training data; no recall, no real embeddings.
- The comparisons are simple methods. The literature on drift (DeDrift, Ada-IVF, SPFresh) splits and reassigns the clusters.

## Review Triage Log

One reviewer without context (Blind Hunter), 13 findings. It verified with its own code.

| # | Finding | Verdict | Evidence and outcome |
|---|---|---|---|
| 1 | The sentence on the limit (m = 1 gives the exact incremental mean) is false with the cosine step size | high | True: the new points weigh 0.55 on average. Corrected the docstring; added a test that shows both things (equality at constant step size, gap with the cosine). |
| 2 | Even at constant step size the limit is not the comparison used | medium | True: the limit is the online mean with centroids that move. Added that comparison and renamed the previous one. |
| 3 | The most natural comparison is missing: mini-batch k-means with true counts | high | True, and it is stronger than the one I was using. Added; the grid is now compared against this. The conclusion "e-means beats the incremental mean" was narrowed to the cases with 20% and 50% of new points. |
| 4 | The comparison stopped at one iteration | medium | True. Added frozen Lloyd with 3 passes and e-means with 3 epochs, with the cost stated. |
| 5 | "Best of the grid" chosen on the same runs | high | True. Replaced with one fixed configuration for all the columns and data types. It is still chosen after the first grid: stated in the limits. |
| 6 | The grid does not bracket the minimum | medium, deferred | True. Stated in the limits; extension recorded in `deferred-work.md`. |
| 7 | The 10 runs are not independent | low | True. Stated in the header of the tables and in the design. |
| 8 | Reference too noisy on the well-separated groups | medium, deferred | True and already known. On those data only the paired comparisons are used; a more solid reference recorded in `deferred-work.md`. |
| 9 | The cells show only the median | low | True. The count of wins gives the sign; stated in the limits that minimal differences cannot be distinguished. |
| 10 | The label of the best one attributed a role to tau for no reason | low | Moot: the row was removed. |
| 11 | Cluster revival is not a fair comparison and is not a neutral forgetting | medium | True. Conclusion 6 reworded as "unsuited to this scenario"; variant that discounts only the clusters hit recorded in `deferred-work.md`. |
| 12 | Old counts and centroids not consistent; the counts cost one pass | low | True. Stated the assumption that the index knows the counts and the inconsistency with the finalized centroids. |
| 13 | Single scenario, favourable to forgetting; no control without drift | high | True. Added the data type without drift, which changed conclusions 2 and 3. The mixed cases remain in the limits. |

## Caveat added after step D

The results of this spec measure the error by reassigning each point to the nearest centroid. An index that reads only the new points does not do that: the vectors already inserted stay in their lists. With that measure, at step D, the advantage of the reduced mass over the classic mini-batch k-means disappears (see `spec-d-sequential-updates.md`). The conclusions of this spec on the best mass therefore hold only if after the update all the vectors are reassigned, an operation that costs as much as one epoch. The conclusion on the naive use and the one on cluster revival remain valid in any case.
