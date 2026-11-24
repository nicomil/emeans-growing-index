---
title: 'Step D: sequential updates'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/journey/spec-4-new-points-only.md'
  - '{project-root}/docs/journey/spec-4b-mass-rule.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** All the experiments so far measure a single update. With few new points the differences between strategies are a few tenths of a point. The real case is a repeated update, and it is not known whether those differences accumulate or vanish: on this depends whether it is worth continuing to work on the mass.

**Approach:** Ten updates in a row, each with new points equal to 5% of the initial data, in which every strategy restarts from its own centroids of the previous round. Three drifts: none, fixed new zone, zone that moves away. The error on all the data is measured after 1, 5 and 10 rounds.

</frozen-after-approval>

## Implementation Notes

**Code**

- `exp_sequence.py`: `uv run exp_sequence.py > results/exp_sequence.md`, about five minutes. Requires the parameters written by `exp_rule.py overlapping` . All the rounds and all the datasets are in `results/exp_sequence.json`.

**Design**

- 50,000 initial points in 32 dimensions, 256 centroids, data without well-separated groups. Ten rounds of 2,500 new points: at the end the new points are a third of the total.
- Three drifts with the same 40 components in the new zone: none; fixed zone shifted by 1.5; zone that moves away by 0.15 at every round.
- Strategies on the new points only: e-means with the default settings; mini-batch k-means starting from the list sizes; e-means with mass 1, with mass from the share rule (about 0.4), with mass 0.2. One strategy that re-reads everything: one warm epoch at every round.
- Reference: e-means from scratch on all the data, 10 epochs, redone at every round. 5 datasets never used before.
- **Two metrics.** "Lists": every point stays in the list it was inserted into, as in an IVF index that does not re-read the vectors already present; it is the realistic measure for those who read only the new points. "Reassigning": every point goes to the nearest centroid, which requires re-reading all the vectors. Steps 4 and 4b had used only the second.
- **"Single shot" control**: the same update done once only with all 25,000 new points.

**Results after ten rounds**

Excess error, median [minimum; maximum] over 5 datasets.

Lists metric:

| Strategy | No drift | Fixed zone | Zone that moves away |
|---|---|---|---|
| initial centroids, never refreshed | +0.36% [0.35; 0.42] | +19.73% [18.52; 22.53] | +10.48% [9.95; 12.18] |
| e-means, default settings | +130.09% [128.04; 133.27] | +166.32% [157.53; 168.17] | +169.87% [164.46; 176.95] |
| mini-batch from the list sizes | +0.18% [0.17; 0.24] | +9.78% [9.39; 11.70] | +6.33% [5.99; 7.50] |
| e-means, mass 1 | +0.20% [0.19; 0.27] | +10.30% [9.90; 12.33] | +6.76% [6.57; 8.00] |
| e-means, mass from the share | +0.30% [0.29; 0.36] | +9.29% [8.98; 11.12] | +6.47% [6.13; 7.70] |
| e-means, mass 0.2 | +0.86% [0.85; 0.93] | +10.43% [9.72; 11.55] | +9.55% [9.12; 10.81] |
| warm on all the data, 1 epoch | +0.59% [0.51; 0.63] | +0.97% [0.84; 1.23] | +1.30% [1.17; 1.63] |

Metric that reassigns everything, for the strategies on the new points only:

| Strategy | No drift | Fixed zone | Zone that moves away |
|---|---|---|---|
| mini-batch from the list sizes | +0.15% | +8.08% | +5.23% |
| e-means, mass 1 | +0.19% | +9.39% | +6.20% |
| e-means, mass from the share | +0.20% | +5.99% | +3.58% |
| e-means, mass 0.2 | +0.48% | +3.38% | +2.72% |

Ten rounds against single shot, lists metric: mini-batch +9.78% against +8.75% with the fixed zone and +6.33% against +6.02% with the zone that moves away; mass 0.2 +10.43% against +8.50% and +9.55% against +7.15%. With no drift the two values coincide for mini-batch and mass 1.

Reads in ten rounds: 25,000 points for the strategies on the new points only, 637,500 for the one that re-reads everything.

**What holds up**

1. **With the realistic metric the advantage of the reduced mass disappears.** In the lists, with the fixed zone, all the strategies on the new points only sit between +9.3% and +10.4% with overlapping intervals; with the zone that moves away and with no drift, mass 0.2 is the worst. Classic mini-batch k-means starting from the list sizes is equal to or better than e-means with any mass tried.
2. **The reason.** A low mass lets the centroids move towards the new points. But the old points stay in their lists and do not follow the centroid: the error of the initial points in their lists rises by +9.6% and +12.7% with mass 0.2, against +2.3% with mini-batch. The gain seen at steps 4 and 4b exists only if all the vectors are reassigned after the update.
3. **Reassigning everything has a cost that makes the trick pointless.** Reassigning means re-reading every vector and comparing it with all the centroids, that is, as much as one epoch costs. At that price one warm epoch on all the data gives +0.97% and +1.30%, against +3.38% and +2.72% for mass 0.2 with reassignment.
4. **Updating with the new points only recovers about half of the degradation, whatever method is used.** With the fixed zone it goes from +19.7% to about +9.8%; with the zone that moves away from +10.5% to +6.3%. Re-reading everything brings it to about +1%.
5. **The accumulation exists but is small.** Ten rounds give an error 0.3-2 points higher than the single shot with the same points. The growth of the error from one round to the next comes mostly from the increase in shifted points. The conclusion written before the review ("the differences accumulate") was wrong.
6. **The naive use is even worse than measured before.** In the lists the error goes from +130% to +170%, even with no drift: the centroids are rewritten and the old points stay in lists whose centroid is elsewhere.

**Consequences for the project**

- Path A (per-cluster mass) loses its motivation: the limit is not choosing the mass well, it is that the points already inserted cannot be moved without re-reading them.
- It becomes clear why the literature on drift (SPFresh, Ada-IVF) locally reassigns only the clusters that change: it is the way to pay for the re-read only where it is needed. It is the only direction left in which e-means might give something in the incremental scenario, and it has not been touched.
- The results that do not depend on the metric remain valid: the warm start that re-reads everything beats starting from scratch at equal cost (step 3), and the naive use on the new points only does damage.

**Limits**

- Only data without well-separated groups; a single combination of n, k and dimension; a single volume per round.
- 5 datasets; seeds of the data and of the algorithm tied together; no paired differences between strategies.
- The lists metric is a quantization error, not the recall of a search: a point in a "wrong" list can still be found by probing more lists.
- The rule from the share is used below the range on which it was calibrated and is in effect a constant (0.40-0.44).
- The strategy that re-reads everything uses the default almost zero mass; with a non-zero mass it might do better.
- The reference sees the new points while it trains, the never-refreshed centroids do not: part of their excess with no drift is this.
- Synthetic data.

## Review Triage Log

One reviewer without context (Blind Hunter), 12 findings. Verified on one dataset with their own code.

| # | Finding | Verdict | Evidence and outcome |
|---|---|---|---|
| 1 | The control that separates accumulation from the increase in shifted points is missing | high | True. Added the single shot: accumulation is worth 0.3-2 points, the rest is volume. Withdrew the conclusion on accumulation. |
| 2 | The error was measured by reassigning all the points, which an index that reads only the new ones does not do | high | True, and it overturns the conclusions on the mass. Added the lists metric as the main measure; added a caveat to the specs of steps 4 and 4b. |
| 3 | The counts carried forward are not those the strategies assume | medium | True. Now the counts are by definition the list sizes, that is, what the index knows; the comparison was renamed accordingly. |
| 4 | "Zone that moves away" generated ten different zones, not monotonic | high | True. The 40 components are drawn once and translated; verified the shift per round (from 0.12 to 1.49, regular). |
| 5 | The column of the initial points had a wrong denominator | medium | True. Now it is compared with the error of the same points on the initial centroids, in their lists. |
| 6 | The reference was used outside the loop | low | True. Added a check on the constant. |
| 7 | Only three rounds reported and saved | medium | True. Now the reference is redone at every round and all the rounds are in the raw file. |
| 8 | Paired differences are missing; seeds tied together | low, deferred | True. Stated in the limits. |
| 9 | The rule from the share is in effect a constant; the rule from the signal is missing | low | True for the first part, stated in the limits. The rule from the signal was discarded at step 4b. |
| 10 | The strategy that re-reads everything is not strong and its cost was hidden | medium | Added the cumulative cost. The variant with non-zero mass stays in the limits. |
| 11 | With no drift the growth of the never-refreshed centroids is not degradation | low | True. Stated at the top of the table and in the limits. |
| 12 | Details: duplicated function, relative path, no verification of the generator | low | Removed the duplicated function, documented the dependency on `exp_rule.py`; the generator was verified by hand, without tests. |
