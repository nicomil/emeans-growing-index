---
title: 'Step 2: check against Faiss e-means'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/journey/spec-1-emeans-numpy-2d.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The comparison between `emeans.py` and the Faiss implementation was done only once, in a temporary environment outside the project. If the code changes, nothing warns that it is no longer equivalent to the original.

**Approach:** Bring the comparison into the project's test suite: same data, same recipe, same number of epochs, median error within 1%.

</frozen-after-approval>

## Implementation Notes

- `faiss-cpu==1.16.0` added to the development dependencies, with a pinned version: the coefficients of the scaling laws are those of this version.
- New test `test_matches_faiss_emeans` in `test_emeans.py`: 30,000 Gaussian points at 32 dimensions, 128 clusters, 3 epochs, 7 seeds. It also checks that batch and initial step size match the `recipe` field of Faiss.
- Faiss is called with `unused_threshold=0.1` to align it with our choice; above 2 dimensions it is also its default value.
- Gaussian data and not well-separated groups, for the reason described in the Surprise section of the step 1 spec.
- Result: median error 24.8958 against 24.8972 for Faiss, a difference of 0.006%.

There is no separate comparison script: the test is enough and runs with the rest of the suite.

The review of this step was done together with that of step 3; the log is in `spec-3-warm-start.md`.
