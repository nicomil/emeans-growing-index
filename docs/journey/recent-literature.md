---
title: 'Activities 6.1 and 6.2: check with Faiss and recent literature'
status: done
created: 2026-11-22
---

# Activities 6.1 and 6.2

## 6.1 The naive use breaks the index with the Faiss code too

`check_faiss_naive.py` repeats the update on the new articles only by calling `NumpyEmeans.train(nuovi, init_centroids=vecchi)` from Faiss 1.16.0, without touching any setting. Recall@10 reading 1% of the index, median over 3 seeds (full table in `results/check_faiss_naive.md`):

| Update | After 1 round | After 5 | After 10 |
|---|---|---|---|
| never refresh | 0.829 | 0.806 | 0.781 |
| hand-rewritten e-means | 0.153 | 0.072 | 0.052 |
| Faiss e-means | 0.144 | 0.070 | 0.052 |

The collapse does not depend on our rewrite. Result 2 of the plan is confirmed and can be written with reference to the shipped code.

## 6.2 Literature and projects that came out after the paper

Search done on 22 November 2026, sixteen days after the paper. I found no study on e-means used incrementally, starting from the existing centroids of an index, or under data drift. I found four relevant things:

| Source | What it does | What it covers of our results |
|---|---|---|
| [h-means](https://github.com/heldernoid/hmeans), independent project | Hierarchical start built on top of e-means: first a few centroids, then splits. Runs on CPU; claims a training error 0.03-6.7% lower than e-means at 5 passes. | "Warm start" in another sense: within a single build, not from an existing index. No updates, no drift. |
| [PISCES](https://huggingface.co/Nabidnur/PISCES), independent technical report | Variant of e-means. Criticises the revival of dead clusters: the reborn centroid is an almost identical copy of the donor. Measures the recall of an IVF index on DEEP1B: equal to e-means within 0.02 points on average. Runs on a 4-core CPU. | Touches cluster revival, but for a defect different from ours (overlapping copies, not recycling of clusters still in use). Recall on images, not on text. No updates. |
| [Milvus request](https://github.com/milvus-io/milvus/issues/55762), opened on 20 November 2026 | Asks to offer e-means as an option for building IVF indexes. A contributor replies that Faiss will be updated "in about a week". | Nothing. It does show, however, that vector engines are about to adopt it: the warning about the incremental use arrives at the right moment. The request itself notes that the timings claimed by the paper do not guarantee a gain in Milvus. |
| [e-means paper](https://arxiv.org/abs/2611.09501), Appendix M | Talks about "drift" of the approximate index used during training at very large scale. | It is another phenomenon, with the same name. It has to be clarified in the text to avoid confusion. |

There remain the works on drift that predate e-means, already known: [DeDrift](https://arxiv.org/abs/2308.02752), [Ada-IVF](https://arxiv.org/abs/2411.00970), [SPFresh](https://arxiv.org/abs/2410.14452). None of them uses e-means.

**Outcome.** The topic does not appear to be covered. The study can be presented as: an independent replication on text and on a laptop, plus a warning and a negative result on the incremental use that nobody has documented yet.

**Limits of the search.** General search engine, three queries, plus the reading of three pages. I did not consult the list of citations of the paper on Semantic Scholar or Google Scholar, nor the discussions in the Faiss repository after the release. Sixteen days is not long: it has to be repeated before publishing.
