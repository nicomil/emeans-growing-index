- source_spec: `docs/journey/spec-1-emeans-numpy-2d.md`
  summary: Measure whether zeroing the epoch sums of split clusters, and skipping cluster revival at the last step, improves the finalized centroids.
  evidence: After a split, donor and child keep accumulating into the epoch sums the points taken from the previous position, so finalization averages two different regions. Faiss 1.16.0 does the same; the reviewer observed no damage because in the test data the splits run out early. Relevant for the warm start, where splits can also happen late.
- source_spec: `docs/journey/spec-3-warm-start.md`
  summary: Add the warm strategy that reads only the new points (or the new ones plus a sample of the old ones), with cost proportional to the share of new data.
  evidence: In exp_warm.py all strategies re-read the whole dataset. The real incremental use case is not measured, and without it there is no knowing whether the initial mass helps where it matters.
- source_spec: `docs/journey/spec-3-warm-start.md`
  summary: Repeat the experiment on data with well-separated groups, with enough seeds to withstand the variance.
  evidence: The overlapping mixture was chosen after seeing that well-separated groups gave an unstable reference (4-8% across seeds). It is the regime in which clusters without a centroid and cluster revival matter, and it was excluded, not studied.
- source_spec: `docs/journey/spec-3-warm-start.md`
  summary: Keep batch and step size fixed across the columns, or add control columns, to separate the effect of the drift from that of the recipe.
  evidence: The scaling law gives batch 1024 and step size 0.25 / 0.23 at 5% and at 20%, batch 2048 and step size 0.34 at 50%. The warm excess is not monotonic along the columns (+1.05%, +1.85%, +0.12%).
- source_spec: `docs/journey/spec-3-warm-start.md`
  summary: Measure the error separately on old and new points, the stability of the clusters, and use a reference at convergence with distinct seeds for data and algorithm.
  evidence: The reviewer measures, at 20%, 30.5 on the old points and 52.2 on the new ones for the old centroids against 31.3 and 32.6 for the warm start; and a 10-epoch reference 0.25% better than the 3-epoch one. Stability is the practical reason for starting warm and it is not measured.
- source_spec: `docs/journey/spec-4-new-points-only.md`
  summary: Choose the initial mass from a drift signal measured on the new points only (error of the new points on the old centroids relative to the typical error of the old ones).
  evidence: The best mass goes from 1-3 with no drift to about 0.1 with a lot of drift. The signal is +1-2% with no drift and +45-72% with drift. Without an automatic rule the fixed configuration makes the no-drift cases worse.
- source_spec: `docs/journey/spec-4-new-points-only.md`
  summary: Extend the grid beyond its edges (m below 0.03, s above 1) and refine it between 0.1 and 1; add mixed cases in which part of the new points comes from the old distribution.
  evidence: The minimum falls on the edge with 5% of new points (s = 1) and with 50% on the well-separated groups (m = 0.03). There is only one kind of drift.
- source_spec: `docs/journey/spec-4-new-points-only.md`
  summary: Try a cluster revival that discounts the mass only of the clusters that receive points, or with a threshold on the true counts.
  evidence: The default cluster revival recycles the old clusters that receive no new points and costs up to 30 points of error; switched off, it does not allow centroids to be reallocated towards the new zone.
- source_spec: `docs/journey/spec-4-new-points-only.md`
  summary: A more solid reference for the data with well-separated groups (best of several restarts, or Lloyd until convergence).
  evidence: On the well-separated groups the 10-epoch reference changes by 8-13% between two seeds of the same dataset and is beaten by 20% by one warm epoch.
- source_spec: `docs/journey/spec-4b-mass-rule.md`
  summary: Try a per-cluster or per-quantile drift signal, in place of the global mean.
  evidence: Two scenarios with the same mean signal (0.36) want masses 0.02 and 0.5. A per-scenario table chosen on the calibration datasets reaches the oracle, so the margin depends on the form of the rule and not on the noise.
- source_spec: `docs/journey/spec-4b-mass-rule.md`
  summary: Evaluate the rule from the share on shares and drift levels not used in the calibration, with masses below 0.01 and a finer grid.
  evidence: Calibration and evaluation share the 15 scenarios; in four cases the error curve is still falling at the lower edge of the grid.
- source_spec: `docs/journey/spec-d-sequential-updates.md`
  summary: Local reassignment: after the update on the new points, re-read and reassign only the lists of the clusters whose centroid has moved beyond a threshold.
  evidence: With the lists metric the error of the initial points rises by 9.6-12.7% when the centroids move (mass 0.2); reassigning everything, the same strategy drops from +10.4% to +3.4%. The cost could be limited to the clusters touched, as SPFresh and Ada-IVF do.
- source_spec: `docs/journey/spec-d-sequential-updates.md`
  summary: Re-measure steps 4 and 4b with the lists metric and, on a real index, with recall at a fixed number of probed lists.
  evidence: Those steps use only the metric that reassigns everything. The lists metric is a quantization error and does not say how much recall is lost.
