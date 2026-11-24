---
title: 'Step 5: check on real embeddings, with the recall of a search'
type: 'feature'
created: '2026-11-22'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context:
  - '{project-root}/docs/journey/brief.md'
  - '{project-root}/docs/journey/spec-d-sequential-updates.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** All the conclusions of the project come from synthetic data and from the quantization error. Four of them fell in review. It is not known which ones hold up on real text, nor how much they are worth in the measure that matters to those who use an index: the recall of a search.

**Approach:** Repeat the comparison between the refresh strategies on a text corpus with real dates, inserted in chronological order, measuring both the error in the lists and recall@10 at fixed search cost. Add the direct comparison between a full rebuild with e-means and with classic k-means.

</frozen-after-approval>

## Implementation Notes

**Code**

- `embed_news.py`: downloads the corpus and computes the embeddings. `uv run --group real embed_news.py`, a few minutes, once only. Writes to `data/`, which is not under version control.
- `exp_real.py`: the experiment. `uv run exp_real.py > results/exp_real.md`, about ten minutes.
- `exp_new_only.py` and `exp_rule.py`: two functions now derive the number of centroids and the dimension from the arguments, instead of from the constants of the synthetic data.

**Data**

- Corpus: HuffPost headlines and summaries, 209,119 articles from 28 January 2012 to 23 September 2022 (`heegyu/news-category-dataset` on Hugging Face). About 30,000 articles a year until 2017, then far fewer.
- Embeddings: `all-MiniLM-L6-v2`, 384 dimensions, normalized vectors.
- 3,000 articles drawn at random and held out of the index serve as queries.

**Design**

- Initial index: the first 100,000 articles, up to 8 February 2015. Then ten rounds of 10,000 articles in date order, up to 1 September 2019: the index doubles. The rounds have the same number of articles, not the same duration: the first covers four months, the last five cover three years, because the corpus thins out after 2017. The articles after September 2019 are left out.
- 2,048 lists (4 times the square root of 200,000, rounded to a power of two, as in Appendix L of the paper): about 50 articles per list at the start, 100 at the end.
- Recall@10: for each query the nearest lists are probed until exactly 1% of the index has been read, and one counts how many candidates are at least as close as the true tenth article. This way the search cost is identical for all strategies, and duplicates and ties (the corpus contains some) do not count as errors.
- Only the queries dated within the period that the index covers are used: 1,536 after one round, 2,136 after five, 2,898 after ten. Recall is therefore not comparable across different rounds, only across strategies within the same round.
- Error in the lists: every article stays in the list it was inserted into, except for the strategies that re-read everything.
- No-drift control: the same 200,000 articles in random order, in an index built on the first 100,000 and never refreshed.
- 3 seeds of the algorithm; the corpus and the queries are fixed.

**Results after ten rounds (index doubled, 2015 → 2019)**

Median over 3 seeds; [min; max] is the variability of the algorithm alone. "Added period": the 1,508 queries dated after the initial index.

| Strategy | Epochs spent in 10 rounds | Error in the lists | Recall [min; max] | Recall, added period |
|---|---|---|---|---|
| never refresh | 0 | +5.61% | 0.781 [0.779; 0.783] | 0.728 |
| never refresh, random order (no-drift control) | 0 | +1.99% | 0.831 [0.828; 0.832] | 0.823 |
| e-means, default settings (new only) | 0.5 | +143.66% | 0.052 [0.052; 0.054] | 0.080 |
| mini-batch from the list sizes (new only) | 0.5 | +2.84% | 0.805 [0.801; 0.806] | 0.765 |
| e-means, mass 0.2 (new only) | 0.5 | +4.87% | 0.808 [0.805; 0.808] | 0.776 |
| warm on all the data, 1 epoch per round | about 8 | +2.64% | 0.824 [0.821; 0.825] | 0.811 |
| from scratch on all the data, 1 epoch | 1 | +3.33% | 0.822 [0.819; 0.822] | 0.810 |
| warm on all the data, 3 epochs per round | about 23 | +0.34% | 0.840 [0.837; 0.840] | 0.829 |
| from scratch on all the data, 3 epochs | 3 | +0.58% | 0.838 [0.837; 0.842] | 0.828 |
| from scratch on all the data, 10 epochs (reference) | 10 | 0 | 0.843 [0.842; 0.843] | 0.835 |

Epochs are in units of the final index. The warm strategies restart at every round from their own centroids, so their cost adds up; the from-scratch ones can be done once only, when needed.

After a single round (10% more articles, 1,536 queries): never refresh 0.829; mini-batch 0.827; one warm epoch 0.798 and from scratch 0.797; three warm epochs 0.826 and from scratch 0.825; reference 0.834.

Full rebuild of the final index with the Faiss implementations, on an M1 Mac with 8 threads. One measurement per seed, error on the training data.

| Method | Median time | Median error |
|---|---|---|
| e-means, 3 epochs | 4.4 s | 0.6099 |
| classic k-means, 3 iterations | 2.8 s | 0.6264 |
| classic k-means, 5 iterations | 4.6 s | 0.6192 |
| classic k-means, 10 iterations | 9.2 s | 0.6136 |
| classic k-means, 25 iterations | 22.7 s | 0.6108 |

**What holds up on real data**

1. **The drift is there and it is measurable.** An index never refreshed ends up at a recall of 0.781 against 0.843 for a rebuilt one: 6.2 points less. The random-order control gives 0.831: of those 6.2 points, 1.2 come from having centroids fitted on half of the data and 5.0 from the drift. On the queries of the added period the loss is almost 11 points (0.728 against 0.835).
2. **The naive use of e-means destroys the index.** Training it on the new articles only starting from the old centroids, with the default settings, takes recall to 0.153 after one round and to 0.052 after ten.
3. **On the new articles only, e-means with reduced mass cannot be told apart from classic mini-batch k-means**: recall 0.808 against 0.805, a difference that three seeds and fixed queries do not allow to be attributed, with a higher error in the lists (+4.87% against +2.84%). Both recover about 40% of the lost recall.
4. **The full rebuild with e-means is the right choice at this scale.** Three epochs give a recall of 0.838, half a point from the reference. With the Faiss implementations, e-means at 3 epochs takes 4.4 seconds and reaches an error of 0.6099; classic k-means in the same time (5 iterations, 4.6 seconds) stops at 0.6192, and to get to 0.6108 it needs 25 of them, that is, 22.7 seconds. At equal error e-means is about 5 times faster on a laptop; the paper claims 8-15 times on 64 cores.
5. **Starting from the old centroids does not show in search.** At equal epochs per round the error is lower by 0.2-0.9 points, but recall is the same within the variability (0.840 against 0.838; 0.824 against 0.822), and the warm start has to be repeated at every round. The warm start here uses the default almost zero mass: with a non-zero mass it was not tried on these data.
6. **A single epoch is not enough.** After the first round, rebuilding with one epoch gives a recall of 0.797-0.798, worse than not refreshing at all (0.829). With 50-100 articles per list at least three epochs are needed.

**Conclusion of the project, at this point**

With e-means the full rebuild costs so little that the incremental shortcuts are not worth it: those that do not re-read the vectors recover less than half of the lost recall, and the only way of using e-means incrementally without precautions does serious damage. The question in the brief, how much to trust the old centroids, has a practical answer different from the one sought: there is no need to trust them, it is better to rebuild.

**Limits**

- A single corpus, a single embedding model, 200,000 vectors. At much larger scales the full rebuild costs more and the balance may change.
- Three seeds of the algorithm with fixed corpus and queries: the variability reported is that of the algorithm. Differences of a few thousandths of recall between close strategies cannot be told apart; an interval over the queries is missing.
- After the first round the recall of the added period rests on 146 queries.
- The error of the new articles on the old centroids includes a part that is not drift: with 50 articles per list in 384 dimensions even articles from the same period, not seen in training, have an error about 5% higher (the reviewer's measurement).
- Short texts (headline and summary), not the document chunks typical of a RAG system. The queries are held-out articles, not user questions: the recall holds for "find similar articles".
- Recall at a single cost level (1% of the index read).
- Timings: one measurement per seed, always in the same order, in the same process, with no associated recall.
- The cost of rewriting the lists for the strategies that re-read everything is not measured.
- The mass 0.2 comes from the calibration on the synthetic data; the rule from the signal of step 4b was not tried again.
- Dataset and model are not pinned to a revision; the embeddings are not under version control.
- No comparison with the methods in the literature that split and reassign clusters.

## Review Triage Log

One reviewer without context (Blind Hunter), 15 findings. Verified on one seed with their own code.

| # | Finding | Verdict | Evidence and outcome |
|---|---|---|---|
| 1 | The stated number of queries was wrong and changes between rounds | medium | True: 1,536, 2,136, 2,898, not 3,000. It is now printed for each round and stated in the design. |
| 2 | The recall of the added period at the first round rests on 146 queries | low | True. Printed and stated in the limits. |
| 3 | [min; max] measures only the noise of the algorithm | medium | True. Stated in the table and in the limits; conclusions 3 and 5 reworded as "cannot be told apart". No bootstrap over the queries. |
| 4 | The no-drift control is missing | high | True. Added the random order: 0.831 against 0.781. Conclusion 1 now separates the 5.0 points due to the drift from the 1.2 due to growth. |
| 5 | The gap between seen and unseen data is not separated from the drift | medium | True. Stated in the limits with the reviewer's measurement. |
| 6 | The 1% limit was exceeded, to a different extent for each strategy | medium | True: up to 6% more reads for the unbalanced lists. Now the last list is read only in part. The recall of the never-refresh strategy dropped from 0.788 to 0.781. |
| 7 | Duplicates and ties not handled | low | True. Recall now counts the candidates at least as close as the true tenth. |
| 8 | The warm rows do not state the cumulative cost and use an almost zero mass | medium | True. Added the column of epochs spent; the mass is stated in conclusion 5 and in the limits. |
| 9 | The cost of the incremental strategies and of rewriting the lists is missing | medium | Added the epochs column. The rewriting cost stays in the limits. |
| 10 | A single point per method in the timing comparison | medium | True. Added k-means at 3, 5, 10 and 25 iterations: conclusion 4 is now expressed at equal time and at equal error. |
| 11 | Weak timing protocol | low | Printed the number of threads and stated the protocol. Repetitions and alternating order not added. |
| 12 | The link between hand-written e-means and the Faiss one is missing | low | Saved the absolute error of the reference in the raw file. |
| 13 | The queries are articles, not user requests | low | True. Stated in the docstring and in the limits. |
| 14 | The rounds are equal in number, not in duration; the 2019-2022 stretch is left out | low | True. Stated in the design and at the top of the tables. |
| 15 | Reproducibility and input checks | low | Added two checks on the embeddings file. Dataset and model revisions not pinned: stated in the limits. |
