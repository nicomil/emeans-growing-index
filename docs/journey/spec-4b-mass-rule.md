---
title: 'Step 4b: choosing the initial mass from a drift signal'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/journey/spec-4-new-points-only.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** From step 4: when updating the centroids with the new points only, the best initial mass depends on how much drift there is, from 1-3 without drift to about 0.1 with a lot. In practice the drift is not known, and a badly chosen fixed mass makes the cases without drift worse.

**Approach:** Measure a drift signal that does not require rereading the old data, fit a rule that derives the mass from it, and evaluate it on data sets different from the fitting ones, including data of a different type. The result may be negative: it has to be reported anyway.

</frozen-after-approval>

## Implementation Notes

**Code**

- `exp_rule.py`: `uv run exp_rule.py overlapping > results/exp_rule_overlapping.md` fits the rules and evaluates them (about a minute and a half); with `separated` it evaluates the same rules, without refitting them, on data with well-separated groups. Parameters in `results/exp_rule_fit.json`; full grids and evaluations in the `.json` files next to it.
- `test_emeans.py`: one test on the fitting procedure.

**Design**

- Signal: mean error of the new points on the old centroids, divided by the mean error of the old points on the same centroids, minus 1. The denominator is a number that the index can keep. Reading the signal costs one more pass over the new points, not counted in the comparisons.
- 15 cases: share of new points 5%, 20%, 50% × five drifts (none; a quarter of the new points from the shifted zone; half; all, zone shifted slightly; all, zone shifted as in step 4).
- A single knob: the mass m, ten values from 0.01 to 10. Step size at a quarter of the one from the scaling law and cluster revival off.
- Four rules: constant mass; from the signal; from the share of new points; from both. Fitted on data sets 0, 1, 2; evaluated on sets 5, 6, 7, never used before (sets 0-4 had been used in step 4).
- Metric: error on all the data relative to the mini-batch k-means with true counts. Negative means better.
- Oracle: the best mass of the grid, chosen by looking at the result.

**Fitted rules**

- constant: m = 0.20
- from the signal: log m = −2.07 − 0.45 · log(signal): m from 0.8 without drift to 0.15 with the strongest drift
- from the share: log m = −1.84 − 0.30 · log(f): m = 0.39 with 5% of new points, 0.26 with 20%, 0.20 with 50%
- from the signal and the share: log m = −2.42 − 0.50 · log(signal) − 0.40 · log(f)

**Results**

Summary over the 15 cases: mean, worst case, and in how many cases the rule does worse than the mini-batch by more than 0.05 points.

| Rule | Overlapping data (same type as the fitting) | Data with well-separated groups (never used for fitting) |
|---|---|---|
| oracle | −1.07%; +0.01%; 0 cases | −5.94%; +0.02%; 0 cases |
| constant mass 0.20 | −0.86%; +0.29%; 7 cases | −2.70%; +1.03%; 7 cases |
| from the signal | −0.92%; +0.11%; 2 cases | −2.60%; +9.04%; 5 cases |
| from the share | −0.87%; +0.18%; 2 cases | −2.88%; +0.23%; 3 cases |
| from the signal and the share | −0.92%; +0.02%; 0 cases | −3.84%; +2.82%; 4 cases |

On the well-separated groups the signal ranges from 1.2 to 5.0 in the cases with drift, against 0.2-0.7 on the fitting data. The rule from the signal extrapolates outside the range on which it was fitted and chooses masses between 0.06 and 0.12; with 5% of new points the best mass is 0.5 and the error worsens by up to +9.04%.

**What holds**

1. **The drift signal, defined this way, is of no use for choosing the mass.** On data of the same type it adds 0.06 points to the constant mass, less than the variability between data sets. On data of a different type it does damage. The reviewer verified that its coefficient is not determined by the fitting: any value between −1.30 and +0.05 gives the same error within 0.05 points, and refitting on the well-separated groups the best coefficient is zero.
2. **Why it is of no use.** The signal is a mean. Two cases with the same signal (half of the new points shifted a lot; all shifted slightly: 0.36 both) want opposite masses, 0.02 and 0.5. And for the same scenario the signal changes sevenfold going from overlapping data to well-separated groups: it is not a measure of drift independent of the data.
3. **The share of new points, on its own, is a better rule.** It requires no measurement, costs no extra reads, and it transfers: on the well-separated groups it has the lowest worst case (+0.23%) and a better mean than the constant mass. The gain over the constant mass is small, though, 0.01 points on the overlapping data and 0.18 on the well-separated groups.
4. **The constant mass 0.2 remains a reasonable choice**: three quarters of the oracle's gain on the overlapping data, half on the well-separated groups. It loses something without drift (up to +0.34%) and on the well-separated groups with few new points (up to +1.03%).
5. **Unexplained margin remains**, especially on the well-separated groups: the oracle scores −5.94%, the best rule −3.84%. It is concentrated in the cases with 50% of new points, where the best mass is 0.01-0.02, at the edge of the grid.

**Answer to the project's question, at this point**

"How much to trust the old centroids as a function of drift": less than the counts would say (mass around 0.2-0.4, not 1), a little less when the new points are many, and fully only if one knows that there is no drift. A rule that reads the drift from the new data was not found.

**Limits**

- Three data sets for fitting and three for evaluation; a single seed of the algorithm per set.
- Fitting and evaluation share the same 15 scenarios: the data change, not the conditions. No share and no level of drift is held out.
- The data with well-separated groups change two things at once, spread of the groups and size of the shift.
- The fitting does not distinguish intermediate masses between two values of the grid, which proceeds in jumps of a factor of 2-2.5; in four cases the minimum is below the lower edge.
- Step size fixed: a rule that also moves the step size was not tried.
- The mean over the 15 cases is dominated by the cases with 50% of new points.
- Error on the training data; no recall, no real embeddings.

## Review Triage Log

One reviewer without context (Blind Hunter), 17 findings. It recomputed the grids and refitted the rules on its own.

| # | Finding | Verdict | Evidence and outcome |
|---|---|---|---|
| 1 | The rule from the share alone is missing | high | True. Added: it is the most robust. It changed conclusion 3. |
| 2 | The coefficient of the signal is not determined | high | True, verified by the reviewer. Reported in conclusion 1. No interval computed in the script. |
| 3 | The signal is a mean and does not separate scenarios that want opposite masses | high | True: 0.36 in both cases, best masses 0.02 and 0.5. Reported in conclusion 2. A per-cluster or per-quantile signal was not tried: recorded in `deferred-work.md`. |
| 4 | Fitting and evaluation separate only the data, not the conditions | medium, deferred | True. Stated in the limits; held-out scenarios recorded in `deferred-work.md`. |
| 5 | The evaluation on the well-separated groups measures an extrapolation | medium | True, and it is the reason for the failure. Written explicitly in the results. |
| 6 | The well-separated groups change two things at once | low, deferred | True. Stated in the limits. |
| 7 | The signal is not calibrated across different problems | high | True. Reported in conclusion 2. |
| 8 | The 0.01 minimum on the signal was not documented | low | True. Documented in the docstring, together with the limit on the mass. |
| 9 | The cost of reading the signal is not counted | medium | True. Stated in the docstring and in the design; it strengthens the preference for the rule from the share, which does not pay it. |
| 10 | The oracle is limited by the grid | medium | True: in four cases the curve is still going down at 0.01. Stated in the limits. |
| 11 | The summary statistics do not measure what they say | medium | Corrected the worst-cases column with a threshold of 0.05 points. Stated that the mean is dominated by the cases at 50%. Minimum and maximum per cell not added. |
| 12 | Sets 3 and 4 had already been used in step 4 | high | True. The evaluation now uses sets 5, 6, 7. The numbers changed slightly. |
| 13 | A single seed of the algorithm per data set | low | True. Stated in the limits. |
| 14 | The from-scratch reference and the fixed configuration of step 4 are missing | low, rejected | The fitted constant mass (0.20) plays the same role as the fixed configuration (0.3); the from-scratch reference is unstable on the well-separated groups. |
| 15 | The raw files did not allow fitting and oracle to be rechecked | medium | True. They now save the full grids of all the data sets. |
| 16 | The parameters file has no provenance | low, rejected | True but of little weight in a study with two commands to launch in order. |
| 17 | No check on fitting and prediction | medium | True. Added a test: the fitting recovers a known rule. The test showed that the fitting does not distinguish masses between two points of the grid. |

## Caveat added after step D

The results of this spec measure the error by reassigning each point to the nearest centroid. An index that reads only the new points does not do that: the vectors already inserted stay in their lists. With that measure, at step D, the advantage of the reduced mass over the classic mini-batch k-means disappears (see `spec-d-sequential-updates.md`). The conclusions of this spec on the best mass therefore hold only if after the update all the vectors are reassigned, an operation that costs as much as one epoch. The conclusion on the naive use and the one on cluster revival remain valid in any case.
