---
title: 'Step 1: e-means written by hand in NumPy, with a 2D animation'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/journey/brief.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The e-means implementation in Faiss 1.16.0 fixes the initial mass of the centroids at 2⁻¹⁶ and spreads the algorithm over many files designed for GPUs and distributed computing. As a result one can neither study the warm start nor understand the algorithm by reading it.

**Approach:** Rewrite Algorithm 1 of the paper (arXiv 2611.09501) in a single short, readable NumPy file, valid for any dimension, and produce an animation on 2D points in which the centroids can be seen moving. The initial mass and the warm start stay out: they are step 3.

</frozen-after-approval>

## Implementation Notes

**Choices made**

- State kept as position `c` and mass `N` instead of as sum `S` and mass `N`. It is the same form used by Faiss and is algebraically equivalent to Equation 2 of the paper. It avoids the 0/0 division that the `S/N` form produces when the step size is 1 and a cluster receives no points.
- Scaling laws (batch and step size) copied with the coefficients shipped in `faiss/contrib/e_means/base.py`, which differ from those in Table 2 of the paper. They are needed in step 2, to compare against Faiss with the same recipe.
- Cluster revival of dead clusters enabled with threshold 0.1 as in the paper. Faiss turns it off when the dimension is ≤ 2, because on 2D data it worsens the error on unseen data; here it stays on because the purpose in 2D is to see the mechanism.
- Donors drawn with `rng.choice` weighted by mass, without replacement. Faiss uses the Gumbel trick: same distribution, less readable code.
- Animation saved as a GIF, one frame every few updates.

**Files**

- `emeans.py` — algorithm and scaling laws.
- `test_emeans.py` — checks.
- `demo_2d.py` — generates `emeans_2d.gif`.
- `pyproject.toml` — dependencies.

**Checks run**

- `uv run pytest -q`: 13 tests passed (5 before the review, 8 added afterwards).
- `uv run demo_2d.py`: GIF of 100 frames, error from 0.809 at the first step to 0.442 after finalization.
- Preview of step 2, against `NumpyEmeans` from Faiss 1.16.0 with cluster revival at 0.1: batch and initial step size identical in all the cases tried (128 and 0.0935 in 2D; 2048 and 0.4182 at 32 dimensions; 4096 and 0.4150 at 64). Median error on Gaussian data at 32 dimensions, 10 seeds: 23.7905 against 23.7771 for Faiss, with overlapping ranges.

**Surprise**

On data with well-separated groups the error changes a lot from one seed to the next, for both implementations: at 32 dimensions, over 20 seeds, from 11.15 to 29.07 for ours and from 11.16 to 33.81 for Faiss's. It depends on how many groups are left without a centroid. With 5 seeds it looked like a 4.5% difference between the two implementations; with 20 seeds and on Gaussian data there is none. Step 2 and the grid of step 4 need many seeds, or data without well-separated groups.

**Useful observation for step 3**

Finalization (line 11 of Algorithm 1) replaces each centroid with the plain mean of the points that were assigned to it during the last epoch. The initial mass therefore does not enter the final result directly: it can influence it only through the path, that is, through which points end up assigned to which centroid. In the warm experiments the effect will have to be measured with and without finalization.

## Review Triage Log

One reviewer without context (Blind Hunter), 12 findings.

| # | Finding | Verdict | Evidence and outcome |
|---|---|---|---|
| 1 | The multiplicative split does not separate a parent at the origin | low | True: `[0,0] * (1 ± eps)` gives two identical copies. Faiss handles it with `_separate_splits`. Fixed with `nextafter` on the first coordinate; test added. |
| 2 | `epochs`, `batch_size`, `alpha0` not validated, cryptic errors | medium | True: `epochs=0` gave `math domain error`, `alpha0=2` made the mass negative. Checks added; test added. |
| 3 | `batch_size or ...` and `alpha0 or ...` treat zero as absent | low | True. Replaced with `is None`; zero is now rejected by the check of item 2. |
| 4 | Shape and content of `x` not checked | low, rejected | A 1D array fails immediately with an explicit error; the NaN check would cost one more pass over data that in this project we generate ourselves. |
| 5 | Cluster revival does not correct the epoch sums | medium, deferred | True, but it is the same behaviour as Faiss (`_apply_splits` does not touch `_pass_sums`) and step 2 requires fidelity. Comment added; recorded in `deferred-work.md` as a variant to measure. |
| 6 | The description in `pyproject.toml` promises the warm start | false | The description is of the project, not of the function; the warm start is step 3 as declared in the spec. |
| 7 | `batch_law` and `step_law` without tests | medium | True: a typo in a coefficient would have gone unnoticed. Added a test with the values read from the `recipe` field of Faiss in three configurations. |
| 8 | Missing tests for `tau=0`, `on_step`, determinism, `k == n`, duplicates | low, rejected | Short branches with no logic of their own; the error on `k` is now covered by the test of item 2. |
| 9 | Weak quality comparisons and misleading comment | low | True for name and comment: test renamed to "plain lloyd" and comment corrected. The test on the gap with `tau=0` was not added: on a single seed it would be unstable, see the Surprise section. |
| 10 | `mse` allocates the whole n×k matrix | medium | True: 1.6 GB already with 200,000 points and 1,024 centroids, that is, at step 5. `mse` now works in blocks of 65,536 rows. |
| 11 | `on_step` receives the live arrays and does not see finalization | low | True. Documented in the docstring; the signature stays unchanged. |
| 12 | Demo without `__main__`, duplicated data, `matplotlib` among the runtime dependencies | low, rejected | It is a script to be launched, not a module to be imported; four duplicated lines do not justify a shared module. |
