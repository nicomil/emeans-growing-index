# Report for the night of 22-23 November 2026

## In one line

The results hold on four datasets (two corpora times two embedding models), with controlled measurements, and on the most recent Faiss code; two claims I had made, however, need to be scaled back. The drafts of the post and of the documentation request are ready and neither has been sent.

## What you will find

| What | Where |
|---|---|
| Results with confidence intervals | `results/SINTESI.md` |
| Minimal reproduction to attach to the documentation request | `docs/repro_emeans_init_centroids.py` |
| How to redo everything | `README.md` |
| Log of the overnight jobs | `data/night.log` |

## What was done

- **Second corpus**: 210,000 arXiv abstracts, 2007-2021, long texts.
- **Second embedding model**: `bge-base-en-v1.5`, 768 dimensions, on the news.
- **Experiment redone from scratch on all three datasets**, with: two levels of search cost (0.1% and 1% of the index read), results saved query by query, confidence intervals, breakdown of the causes of the damage, measurement also with the lists rebuilt.
- **Timings measured on an idle machine**, one job at a time: six repetitions in alternating order, machine load recorded, k-means at seven different numbers of iterations.
- **Check of the measurement**: with the same number of lists probed, the recall computed by our code matches that of a real Faiss IVF index to the fourth digit, on all three datasets. The fixed-share reading used in the tables has no equivalent in Faiss: it is verified by a test against an obvious, slow version.
- **Fix demonstrated with the Faiss code**, not only with our rewrite.
- **Generic comparison and update size**: the same update done with k-means, and with 50,000 new texts instead of 10,000.
- **Three independent reviews**: of the overnight code, of the draft of the documentation request read "as a maintainer", and a final one on the documents. They led to dozens of corrections; the outcomes are in `docs/journey/spec-6-consolidation.md`.

## What holds

Recall@10 reading 1% of the index, after ten updates (index doubled). In this table the values are means over three seeds, as in `results/SINTESI.md`; the `exp_real_*.md` files, the documentation request and the checks report medians, which can differ by one thousandth. The 95% intervals over the queries are in `results/SINTESI.md`: about ±0.008 on the news, ±0.005 on arXiv.

| | News, 384 dim. | arXiv, 384 dim. | News, 768 dim. |
|---|---|---|---|
| Never updating | 0.781 | 0.918 | 0.746 |
| Same texts in random order (no drift) | 0.830 | 0.939 | 0.807 |
| Naive use of e-means, lists rebuilt | 0.434 | 0.744 | 0.389 |
| Naive use, lists left as they are | 0.052 | 0.069 | 0.049 |
| Classic mini-batch on the new texts only | 0.804 | 0.930 | 0.770 |
| Rebuild from scratch, e-means 3 epochs | 0.839 | 0.943 | 0.814 |
| Rebuild from scratch, e-means 10 epochs | 0.843 | 0.945 | 0.821 |

1. **Drift has a cost**, to a different extent depending on the corpus: 6 points of recall on the news, almost 8 with the larger model, less than 3 on arXiv. Most of it is real drift, not simply growth of the index.
2. **The naive use of e-means ruins the index**, on all three datasets and even when the lists are rebuilt. After a single update of 10,000 texts the recall loses between 30% and 58%.
3. **The damage is largely specific to e-means.** A single update, lists rebuilt, median recall:

   | Centroids updated on the new texts only | News, 384 dim. | arXiv, 384 dim. | News, 768 dim. |
   |---|---|---|---|
   | no update | 0.828 | 0.931 | 0.792 |
   | e-means from the old centroids (naive use) | 0.417 | 0.656 | 0.332 |
   | e-means from random rows, without old centroids | 0.472 | 0.733 | 0.381 |
   | k-means, one iteration from the old centroids | 0.680 | 0.881 | 0.604 |
   | Faiss e-means with initial mass and moving average | 0.827 | 0.932 | 0.792 |

   Fitting 2,048 centroids to 10,000 texts makes things worse with any algorithm, but e-means loses much more than k-means and does no better than a start without old centroids. With 50,000 new texts the damage shrinks and remains: 0.723 against 0.806 on the news, 0.892 against 0.929 on arXiv, 0.657 against 0.773 with the 768-dimension model.
4. **The fix is demonstrated with the Faiss code.** The starting centroids have an almost zero weight, and the result returned is the average of the new texts only. By giving the centroids a weight and reading the moving average, the same Faiss code goes, after ten updates, from 0.052 to 0.807 on the news and from 0.069 to 0.930 on arXiv (medians). How much each of the two changes weighs, and how much cluster revival does, is measured only with our rewrite: the initial weight matters most, removing the final averages alone changes nothing, revival makes things worse with the lists left as they are and better with the lists rebuilt.
5. **Once the defect is fixed, e-means is worth as much as classic mini-batch**: the difference is between 1 and 5 thousandths of recall, in one case to the disadvantage of e-means; sometimes distinguishable from noise, never of practical weight.
6. **Rebuilding from scratch is the right choice**: three epochs get within 0.2-0.7 points of the ten-epoch reference. Training the centroids takes 4-7 seconds; the reassignment of the vectors is not included in that time.
7. **Starting from the old centroids while re-reading everything changes little or nothing.** With the 384-dimension model, on both corpora, no difference in recall compared with starting from scratch. With the 768-dimension model, giving the old centroids the steady-state mass gains half a point (0.819 against 0.814), little but consistent across seeds. The price is redoing three epochs at every update.

## What needs to be scaled back

**"e-means is 5 times faster."** It is true for the quantization error: three epochs of e-means (4.3 seconds of centroid training) give an error that k-means does not reach in 25 iterations (22.6 seconds). The difference in error is small, 0.16%, but it repeats in all six repetitions. For recall it depends on how much of the index is read:

| At equal recall | News, 384 dim. | arXiv, 384 dim. | News, 768 dim. |
|---|---|---|---|
| reading 0.1% of the index, k-means takes | 3.2 to 4.2 times as long | 2.5 to 3.2 times as long | more than 4.4 times as long |
| reading 1% of the index, k-means takes | 0.6 to 1.1 times as long | 1.1 to 2.1 times as long | 0.5 to 0.9 times as long |

With 1% of the index read the advantage disappears on the news and remains, up to a factor of 2, on arXiv. With 0.1% the recall differences on which the ratios rest are a few thousandths: only on arXiv is the gap larger than the variability across seeds. The post says it in these terms.

The timing comparison is between a Python loop (e-means in Faiss) and C++ code (k-means): it penalises e-means.

**"Recall collapses from 0.83 to 0.05."** That number holds if after the update the vectors stay in the lists they were in, something Faiss does not offer and that an expert reader would contest. The defensible number is with the lists rebuilt: from 0.83 to 0.42 after one update. The post and the documentation request use that one.

## How the documentation request changed

The "as a maintainer" review showed that the first draft would have been dismissed as misuse. Now:

- it is a **documentation request**, with an optional proposal, not a bug report: the behaviour is consistent with the paper, which states that it gives the starting point a minimal weight;
- it acknowledges that the two facts are already written in the code, and asks for their consequence to be written down;
- it shows the cause with the Faiss code;
- it admits that the fix is of little use in practice, because rebuilding is better: this is why the note matters more than the function.

## The test on the most recent Faiss code (added on the morning of the 23rd, with your authorisation)

Faiss built from source at commit 16a95d6 of the main branch, the one that changes cluster revival, in a separate environment (`vendor/faiss_venv`); the project environment stays on 1.16.0. One update of 10,000 texts, lists rebuilt, median recall:

| | News, 384 dim. | arXiv, 384 dim. | News, 768 dim. |
|---|---|---|---|
| no update | 0.828 | 0.931 | 0.792 |
| naive use, Faiss 1.16.0 | 0.417 | 0.656 | 0.332 |
| naive use, main branch | 0.512 | 0.784 | 0.421 |
| e-means from random rows, main branch | 0.495 | 0.769 | 0.396 |
| initial mass and moving average, default revival of the main branch | 0.723 | 0.886 | 0.665 |
| initial mass and moving average, revival by mass or switched off | 0.827 | 0.932 | 0.792 |

1. **The warning also holds on the most recent code**, with milder numbers: the recall loses between 16% and 47% (between 30% and 58% in 1.16.0), and the naive use remains on a par with a start from random rows.
2. **Something new.** On the main branch the two changes are no longer enough: the new revival moves the centroids that have not yet received texts, whatever weight they have. Going back to revival by mass, or switching it off, the damage disappears as in 1.16.0. The documentation request says so, and it is useful information for those who maintain that code.

On the main branch only the single update and the synthetic reproduction were redone, not the ten updates in sequence nor the timings. Files: `results/check_naive_baselines_*_main.md`, `results/check_main_revival_*.md`, `results/repro_main.md`.

## The fourth dataset: arXiv with the 768-dimension model

It arrived on the morning of the 23rd: the machine restart at about 06:11 had interrupted the queue, which was resumed at 09:16 and finished at 10:35 with no failed jobs. The tables above stay at three columns; these are the values of the fourth, all in agreement.

| | arXiv, 768 dim. |
|---|---|
| After ten updates: never updating | 0.928 |
| same texts in random order | 0.943 |
| naive use of e-means, lists rebuilt / left as they are | 0.773 / 0.064 |
| classic mini-batch on the new texts only | 0.937 |
| rebuild from scratch, 3 epochs / 10 epochs | 0.946 / 0.947 |
| One update of 10,000 texts: no update | 0.937 |
| e-means from the old centroids, Faiss 1.16.0 / main branch | 0.657 / 0.785 |
| e-means from random rows | 0.754 |
| k-means, one iteration from the old centroids | 0.889 |
| Faiss e-means with initial mass and moving average | 0.937 |
| One update of 50,000 texts: naive use against no update | 0.905 against 0.934 |
| Timings: e-means 3 epochs / k-means 25 iterations | 6.4 s / 28.8 s |
| At equal recall, k-means takes: 0.1% read / 1% read | more than 4.5 times as long / 2.1 to 2.7 times as long |

Three things change slightly compared with what is written above:

- at equal recall with 1% of the index read, the advantage of e-means reaches a factor of 2.7 (before, the maximum was 2.1): the post now says "between half and almost three times";
- with 50,000 new texts the damage of the naive use ranges from 3% to 15% (before, from 4%);
- the half point gained by the warm start with steady-state mass at 768 dimensions holds for the news; on arXiv it is a tenth of a point. Three epochs from scratch get within 0.1-0.7 points of the reference.

The timings of this dataset were measured during the day, with the machine in use: the recorded load (median 2.1, maximum 5.5) is in line with the overnight one (median 1.9-2.4) and the intervals are just as narrow (6.4 s [6.4; 6.5]).

## The large scale: 1.5 million texts (23 and 24 November)

To remove the most contestable limits (small indexes, no real questions, no comparison with the literature) the experiment was redone at a larger scale with `exp_scale.py`, which uses Faiss code only: 800,000 initial texts, 10 updates of 75,000, 16,384 centroids, still on the MacBook Air M1 with 16 GB.

Two archives: all the arXiv abstracts from 2007 to 2021 in date order (1,585,373 texts, real drift), and 1,600,000 MS MARCO passages in random order (no drift) queried with 3,000 real questions from Bing users.

Recall@10 after the 10 updates, Faiss 1.16.0. arXiv: mean of 3 seeds, spread across seeds at most 0.007. MS MARCO: one seed.

| Strategy | arXiv, 1% read | arXiv, 0.1% read | MS MARCO, 1% read | MS MARCO, 0.1% read |
|---|---|---|---|---|
| never updating | 0.989 | 0.867 | 0.928 | 0.807 |
| naive use of e-means, lists left as they are | 0.085 | 0.056 | 0.080 | 0.055 |
| naive use of e-means, lists rebuilt | 0.944 | 0.608 | 0.830 | 0.568 |
| e-means with initial mass and moving average, lists left | 0.991 | 0.880 | 0.929 | 0.807 |
| DeDrift-Lazy | 0.991 | 0.878 | 0.929 | 0.808 |
| DeDrift-Hybrid | 0.991 | 0.886 | 0.929 | 0.809 |
| from scratch, e-means 3 epochs | 0.992 | 0.898 | 0.932 | 0.814 |
| from scratch, e-means 10 epochs | 0.992 | 0.903 | 0.934 | 0.823 |

What it says:

1. **The trap holds at large scale and with real questions.** With the lists left as they are the recall goes to 0.08 on both archives. With the lists rebuilt the naive use loses 4.5 points on arXiv and 10 on MS MARCO reading 1% of the index, 26 and 24 points reading 0.1%. On MS MARCO there is no drift: the damage comes entirely from the update, not from the data.
2. **"Never updating" costs little here.** On arXiv it loses 0.3 points at 1% and 3.6 at 0.1% compared with the rebuild; on MS MARCO, without drift, less than one point. At 1% read (164 lists out of 16,384) the operating point is almost saturated: the column that separates the strategies is 0.1%.
3. **The e-means fix is worth as much as DeDrift-Lazy** (0.880 against 0.878) and stays 0.6 points below DeDrift-Hybrid; the rebuild from scratch is above all of them.
4. **On the Faiss main branch** (`results/exp_scale_arxiv-full_seed0_main.md`, one seed) the naive use gives 0.067 with the lists left and 0.953 rebuilt. Our fix is no longer enough there (0.091 and 0.975), as already seen at small scale: the new cluster revival moves the centroids that receive no texts.

**DeDrift is rewritten by me from the text of the paper**, because no published code appears to exist. The paper does not say how many k-means iterations Split uses nor where it starts from. `check_split.py` measures how much they matter: with 5, 10 or 25 iterations Hybrid gives 0.883-0.885 (0.1% read); starting from the old centroids instead of from random points it drops to 0.878. The choice made is therefore the one most favourable to DeDrift.

**Timings on an idle machine** (`results/bench_scale_*.md`, night of the 24th, load at most 2.0, two repetitions): one pass over the 1,550,000 texts costs 59 s with e-means and 55 s with k-means; reassigning all the vectors 55 s. Rebuilding from scratch with e-means at 3 epochs and reassigning therefore takes about 4 minutes.

| | Training time | arXiv, 1% / 0.1% | MS MARCO, 1% / 0.1% |
|---|---|---|---|
| e-means, 3 epochs | 178 s | 0.993 / 0.900 | 0.931 / 0.814 |
| e-means, 10 epochs | 590 s | 0.992 / 0.902 | 0.936 / 0.820 |
| k-means, 5 iterations | 277 s | 0.991 / 0.893 | 0.937 / 0.813 |
| k-means, 10 iterations | 553 s | 0.992 / 0.898 | 0.937 / 0.820 |
| k-means, 25 iterations | 1,382 s | 0.992 / 0.902 | 0.939 / 0.824 |

The speed advantage of e-means depends on the archive, as at small scale. On arXiv 3 epochs (178 s) give the recall of k-means at 10-25 iterations (553-1,382 s). On MS MARCO they do not: reading 1%, 5 iterations of k-means are enough to beat e-means at 10 epochs, and at 0.1% e-means at 3 epochs is worth k-means at 5 iterations, an advantage of one and a half times.

## What was not done

1. **The long article** foreseen by the plan.
2. **Scales beyond 1.5 million vectors**, indexes with compression, other methods from the literature on drift (Ada-IVF, SPFresh).

## Limits that remain

- One laptop; indexes of 200,000 vectors with three seeds per dataset, plus two archives of 1,550,000 (arXiv with three seeds, MS MARCO with one).
- The confidence intervals concern the queries, not the variability across corpora.
- The queries are held-out texts from the corpus, not questions, except on MS MARCO. MS MARCO has no dates: drift is missing there.
- DeDrift is a rewrite from the paper, not the authors' code.
- English texts only.
- "Lists rebuilt" means rebuilt once, at measurement time, and not after every update. Whoever rebuilds the lists has all the vectors at hand and could retrain on all of them: it is the case most favourable to the naive use, not the most realistic one.
- The update of 10,000 texts with 2,048 centroids (about 5 texts per centroid) is below the range on which the scaling laws of e-means were tuned (from 100,000 rows upwards).
- A single operating point for the search: IVF index without compression, two shares of vectors read.
- Datasets and models are not pinned to a revision.

## What to decide

1. **The post**: the long version was chosen. Is the text fine? The repository must be made public first, because the post cites it.
2. **The documentation request**: you send it. The test on the main branch is done; what remains are the items of the list at the top of the draft (paste the script, the link to the repository, check that an identical request does not already exist).
3. **The long article** foreseen by the plan: the materials are all there; it was not written this night.

## State of the queue

Finished at 10:35 on 23 November, no failed jobs. Log in `data/night.log`.

The large-scale queue (`run_night4.sh`) finished at 06:37 on 24 November, no failed jobs. Log in `data/night4.log`.
