---
title: 'Step 3: initial mass and warm start on synthetic drift'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/journey/brief.md'
  - '{project-root}/docs/journey/spec-1-emeans-numpy-2d.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `emeans.py` always starts from random centroids with almost zero mass. One cannot restart from existing centroids nor decide how much they weigh, so the project's question is not yet measurable.

**Approach:** Add to `emeans` the initial centroids, their mass and the option to skip finalization. Then a first experiment on synthetic data in which the share of new points is known, to see whether the warm start pays off and in which direction mass and step size move. The full grid and the search for the rule stay in step 4.

</frozen-after-approval>

## Implementation Notes

**Code**

- `emeans.py`: three new parameters in `emeans`. `init` are the centroids to restart from; `init_mass` is a number or a vector of k values; `finalize=False` skips line 11 of Algorithm 1. Without these parameters the behaviour is the same as before.
- `test_emeans.py`: three new tests: effect of the mass, wrong arguments, equivalence between huge mass with finalization and one Lloyd pass.
- `exp_warm.py`: the experiment. It is launched with `uv run exp_warm.py` and takes about one minute.

**Units of the mass**

The mass of a cluster is the moving average of the number of points it receives per batch. At steady state it is about `batch_size × share`, where the share is the fraction of points that belongs to the cluster. In the experiment "mass m" means `m × batch_size × share × (1 − f)`, with the share measured on the old data and f the fraction of new data: in a batch of the updated data the old points are only a part. Mass 1 is equivalent to a run already under way; mass 0 is an almost zero mass, like the one Faiss assigns to the initial centroids (2⁻¹⁶; here 10⁻¹⁰, the value from the paper).

**Experiment design**

- Old data: 50,000 points at 32 dimensions from a mixture of 200 overlapping Gaussians. New data: 40 Gaussians shifted by 1.5 in 8 dimensions, in such a quantity as to be 5%, 20% or 50% of the total.
- Old centroids: e-means from scratch, 5 epochs, on the old data only. 256 clusters.
- All the strategies compared spend one more pass over the updated data; the warm ones inherit the 5 epochs already spent on the old data. The reference is e-means from scratch with 3 epochs: it is a term of comparison, not the minimum reachable.
- 10 seeds; old data and old centroids change with the seed. The excess over the reference is computed seed by seed, on the same data; median, minimum and maximum are reported.

**Results**

Excess error over the reference, with finalization: median [minimum; maximum] over 10 seeds.

| Strategy | 5% new | 20% new | 50% new |
|---|---|---|---|
| old centroids, no recomputation | +1.85% [+1.68; +2.16] | +12.03% [+10.98; +12.67] | +30.92% [+28.39; +32.45] |
| one Lloyd pass from the old ones | +1.24% [+1.00; +1.47] | +6.70% [+5.82; +7.24] | +12.45% [+10.80; +13.16] |
| from scratch, 1 epoch | +3.44% [+3.00; +3.65] | +3.45% [+3.22; +3.59] | +2.06% [+1.85; +2.32] |
| warm, mass 0 | +1.05% [+0.76; +1.34] | +1.85% [+1.42; +2.36] | +0.12% [−0.06; +0.45] |
| warm, mass 1 | +0.65% [+0.44; +0.82] | +2.35% [+1.57; +2.67] | +0.03% [−0.19; +0.25] |
| warm, mass 10 | +0.61% [+0.51; +0.96] | +3.13% [+2.88; +3.78] | +1.06% [+0.51; +1.56] |
| warm, mass 100 | +0.65% [+0.49; +1.03] | +4.04% [+3.63; +4.88] | +2.60% [+2.16; +3.90] |
| warm, mass 1, step size/4 | +0.71% [+0.51; +0.92] | +4.39% [+4.07; +4.90] | +3.41% [+2.77; +4.62] |
| warm, mass 10, step size/4 | +0.85% [+0.69; +1.12] | +6.05% [+5.36; +6.46] | +9.18% [+8.48; +10.09] |

Without finalization the order is the same. The most useful rows: from scratch, 1 epoch gives +2.16% [+1.86; +2.32], +2.07% [+1.95; +2.21], +1.21% [+1.11; +1.56]; warm with mass 0 gives +0.83%, +1.28%, −0.15%.

The three columns do not differ only in the share of new data: the scaling law chooses batch 1024 and step size 0.25 at 5%, 1024 and 0.23 at 20%, 2048 and 0.34 at 50%. The irregular trend along the columns therefore cannot be attributed to drift alone.

**What holds**

1. For the same extra cost, the warm start beats the start from scratch. The ranges do not touch in any column, already with the almost zero mass, which is not a variant chosen after the fact.
2. With 20% and 50% of new data it also clearly beats the single Lloyd pass from the old centroids. With 5% only mass 1 separates it; with mass 0 the ranges overlap.
3. Mass 100 and step size reduced to a quarter get worse with 20% and 50% of new data.
4. With a single epoch from scratch, finalization worsens the error, with disjoint ranges in all columns. With a single epoch "the last epoch" is the whole run, so the mean includes the points assigned when the centroids were still far away.

**What does not hold yet**

- That mass 1 is better than mass 0 with little new data and worse with a lot. The medians go in that direction (+0.65% against +1.05% at 5%; +2.35% against +1.85% at 20%), but the ranges overlap. A test on the seed-by-seed differences is needed.
- That reducing the step size always makes things worse: with 5% of new data there is no measurable difference.

**Understood thanks to the review**

With finalization enabled the mass does not measure "how close I stay to the old centroids". The result is the means of the last epoch. With a huge mass the centroids do not move during the epoch and finalization produces exactly one Lloyd pass from the old centroids (verified, it is now a test). In the table with finalization, therefore, increasing the mass moves the result from the "mass 0" row towards the "one Lloyd pass" row, which is worse. The mass as a knob of trust in the past makes full sense only without finalization.

**Surprise**

The first version of the data had the means of the Gaussians too spread out: 240 well-separated groups for 256 centroids. In that regime the reference itself varied by 4-8% from one seed to the next, 10 epochs gave a worse error than 3, and the warm start seemed to beat the reference by 18%. The current data have means closer than the radius of the noise and the reference varies by 0.4%.

This has a cost: the results hold for data without well-separated groups. The regime with well-separated groups, where the clusters left without a centroid matter, was excluded after seeing the numbers, not studied. It has to be taken up again with more seeds.

The trial done before starting the project (warm start worse than the start from scratch, 62.90 against 62.76) was on well-separated groups and with a single seed: it is not a valid refutation of these results, and these do not refute it for that regime.

**Limits**

- A single type of synthetic data, a single combination of n, k and dimension.
- All the strategies reread the whole data set. The real incremental use case is missing: warm starting while reading only the new points, with a cost proportional to how many there are.
- The overall error on the training data is measured. It is not separated between old and new points, there is no error on unseen data nor recall of an index.
- The same seed drives data and algorithm, so the two sources of variability are not separated.
- The step size was only reduced, never increased.

## Review Triage Log

One reviewer without context (Blind Hunter), 19 findings, on steps 2 and 3 together. It reran the experiment.

| # | Finding | Verdict | Evidence and outcome |
|---|---|---|---|
| 1 | Ratio of medians instead of a paired comparison | medium | True: each seed has its own data. The excess is now computed seed by seed. |
| 2 | No measure of dispersion | medium | True, and some of my conclusions did not hold. The table reports minimum and maximum; the conclusions were split between what holds and what does not. |
| 3 | The 3-epoch reference is not a minimum | medium, deferred | True: the reviewer measures −0.25% with 10 epochs. Clarified in the text that it is a term of comparison; reference at convergence deferred to step 4. |
| 4 | "Equal cost" does not count the epochs already spent | low | True. Corrected the docstring and the label of the zero-cost strategy. |
| 5 | The strategy with cost proportional to the new data is missing | medium, deferred | True and it is the real use case. Recorded in `deferred-work.md`. |
| 6 | The share of new data is confounded with batch and step size | medium, deferred | True: the scaling law changes batch and step size between columns. Stated next to the results; columns with a fixed recipe deferred to step 4. |
| 7 | "Mass 1" does not mean the same across columns | medium | True: the factor 1 − f was missing. Fixed; the numbers were recomputed. |
| 8 | Data chosen after seeing the results, critical regime excluded | medium, deferred | True. Stated in the Surprise section; regime with well-separated groups recorded in `deferred-work.md`. |
| 9 | Column of empty clusters always at zero | low | True. Removed. |
| 10 | The overall error hides the trade-off between old and new points | medium, deferred | True: the reviewer shows that the old centroids score 30.5 on the old ones and 52.2 on the new ones. Recorded in `deferred-work.md`. |
| 11 | Six warm variants against one from scratch, chosen after the fact | low | True in general; conclusion 1 now rests on mass 0 alone, fixed at the outset. |
| 12 | The same seed drives data and algorithm | low, deferred | True. Recorded in `deferred-work.md`. |
| 13 | With finalization, a huge mass is equivalent to one Lloyd pass | medium | True, verified. Added the test and the section "Understood thanks to the review". |
| 14 | The docstring does not warn that with finalization the mass does not limit the displacement | medium | True. Warning added. |
| 15 | The label "stock Faiss" is not verified | low | True: Faiss uses 2⁻¹⁶, not 10⁻¹⁰. Label changed, constant `INIT_MASS` reused. The direct comparison with `NumpyEmeans.begin` was not done. |
| 16 | Incomplete validation of the new parameters | low | Fixed the case `init_mass=nan`, with a test. The others rejected: errors already explicit or harmless cases. |
| 17 | 1% tolerance in the test against Faiss too wide | medium | True: with cluster revival off the gap is 0.8% and the test passed. Brought to 0.2%; removed the `print`. |
| 18 | Warm start tests not extensive enough | low | Added vector mass, finalization enabled and a check that `init` is not modified, in the test of item 13. The rest rejected. |
| 19 | Duplicate work between the two tables | low | True. The two variants are now computed in the same run: from 95 to 54 seconds. |
