---
title: "e-means and indexes that change: refresh or rebuild?"
status: approved
created: 2026-11-22
updated: 2026-11-24
---

# Project brief: e-means and indexes that change

## Summary

e-means is a variant of k-means published by Meta FAIR on 6 November 2026 (arXiv 2611.09501) and shipped in Faiss 1.16.0. It promises to build the groups of a vector index in a tenth of the passes over the data. The paper studies it on static datasets.

This study tries it in the situation in which an index actually lives: documents keep arriving and topics change. The starting question was how far the old centroids can be trusted in order to avoid recomputing them. After five steps of experiments, on synthetic data and on 200,000 real newspaper articles, the answer is a different one: it is not worth looking for shortcuts. With e-means the full rebuild costs so little that it is the right choice, and the most obvious way of using it to refresh an index ruins it.

The study is worth something for three things: an independent check of e-means on real text and on a laptop, a practical warning that nobody has documented yet, and the honest account of the paths tried and abandoned.

## The problem

A cluster-based index (IVF) splits the vectors into lists, each represented by a centroid. When new documents on new topics arrive, the centroids stop describing the data well and search gets worse. The remedy is to recompute the centroids, an operation that is expensive with classic k-means and is therefore put off.

e-means reduces that cost. Three questions remain, however, that the paper does not answer:

- How much is really lost by not recomputing, on a real text corpus?
- Can e-means be used to refresh an index by reading only the new documents?
- Does starting from the old centroids save anything?

These are practical questions, and they become urgent because vector engines are adopting e-means: in Milvus the request was opened on 20 November 2026.

## What we did

- Rewrote e-means in a short NumPy file, checked against the Faiss implementation, so as to be able to change what Faiss does not expose.
- Measured the refresh strategies on synthetic data with controlled drift, and then on HuffPost headlines and summaries from 2012 to 2019, inserted in date order into an index that doubles from 100,000 to 200,000 articles.
- Measured the error the way a real index sees it, with every document staying in the list it was inserted into, and the recall of a search at fixed cost.
- Put every step through an independent review, which brought down four intermediate conclusions.

## What we found

1. **e-means keeps its promise on a laptop and on text too.** On 200,000 vectors, three epochs take 4.4 seconds; classic k-means takes 22.7 to reach the same error. The recall of the index rebuilt with three epochs is 0.838, against 0.843 with ten.
2. **Not refreshing has a measurable cost.** In four and a half years recall drops from 0.843 to 0.781; on recent queries it loses almost 11 points. Five of the six points lost are topic drift, one comes from the mere growth of the index.
3. **The most obvious incremental use destroys the index.** Passing the old centroids to e-means and training it on the new documents only takes recall from 0.83 to 0.15 at the first refresh and to 0.05 after ten. It happens with the Faiss code too, without touching anything. There are two causes: the starting centroids have an almost zero weight, and the mechanism that recovers empty clusters recycles those that receive no new documents, even though they still contain the old ones.
4. **The shortcuts do not hold up.** Once the defect is fixed, e-means on the new documents only does no better than classic mini-batch k-means: both recover about 40% of the lost recall. A rule that chooses how much to trust the old centroids based on the drift was not found. Starting from the old centroids while re-reading everything lowers the error a little but does not change recall.

There is only one practical consequence: rebuild the index from scratch with e-means, with at least three epochs, whenever it is needed.

## How it is told

Hybrid thread, approved on 23 November 2026. Title and opening are practical: refresh or rebuild? The central sections instead follow the question the project started from, "I already have good centroids, can I reuse them?", through the three ways tried:

1. passing them to e-means and training on the new documents only: the index breaks;
2. the same, giving them a weight: it works, but no better than classic mini-batch;
3. passing them to e-means while re-reading everything: slightly lower error, recall identical to starting from scratch.

The practical answer closes the journey: rebuild.

## What sets it apart

- The literature on index drift (DeDrift, Ada-IVF, SPFresh) predates e-means and uses images, video or recommendations. The works that came out after the paper, as far as was found by 22 November 2026, do not deal with updates or drift.
- Everything runs on a laptop and can be redone with a few commands.
- It also tells the mistakes: among them, an error measure that for two steps made us believe in an advantage that did not exist.

There is no theoretical contribution. The value is in the check, in the warning and in the timing.

## Who it is for

- **Those who run a cluster-based vector index** and have to decide whether and how to adopt e-means.
- **Those who develop vector engines**, because the warning concerns a use that will come naturally to their users.
- **Those who study or teach these systems**: the short code and the animation show how the algorithm works.

Those who use graph indexes (HNSW), that is, most small and medium RAG projects, are not directly affected. For this reason the study page (`docs/study.html`) opens with a context preamble: what a RAG system is, how the two kinds of index work, when one moves from one to the other, and where the study sits.

## Success criteria

1. The four results repeat on a second corpus, or it is stated where they do not repeat.
2. Every number in the text has an uncertainty interval and a source in the repository.
3. A reader can redo every table with one command.
4. There is a write-up that a technical person reads to the end and comes away from knowing what to do.

## Scope

**In:** second corpus (arXiv abstracts); intervals on recall; recall at two cost levels; repeated timings; the write-up; final review.

**Out:** a different mass for each cluster; reassignment of only the clusters that change; scaling law for the incremental case; direct comparison with DeDrift, Ada-IVF and SPFresh; Italian corpus; GPU. They are to be cited as future work.

## Risks and unknowns

- All the results on real data come, for now, from a single corpus of short texts. On longer texts they might change.
- At scales much larger than 200,000 vectors the full rebuild costs more and the practical conclusion may not hold.
- The search of the recent literature was quick, and sixteen days after the paper is not long: it has to be repeated before publishing.
- The queries used are articles held out of the index, not user questions.

## Where it can go

If the second corpus confirms the results, the natural step is a documentation request in the Faiss repository about the incremental use. The research direction left open is local reassignment: refresh with the new documents and re-read only the lists whose centroids have moved.

## After the brief (24 November 2026)

The work went beyond this brief. What changed, with the numbers in `results/`:

- **The results repeat** on a second corpus (arXiv abstracts) and with a second embedding model (`bge-base-en-v1.5`), four datasets in all.
- **Finding 3 was scaled back.** The drop from 0.83 to 0.05 holds when the old vectors stay in the lists they were added to. With all vectors reassigned to the refreshed centroids, one naive refresh takes recall from 0.83 to 0.42 on the news. Both conditions are now reported side by side.
- **Two items listed as out of scope were done**: a comparison with DeDrift, rewritten from the paper because no public code was found, and a larger scale, 1.55 million vectors with 16,384 centroids, on arXiv and on MS MARCO with real user queries.
- **The speed claim is narrower** than "a tenth of the passes": at equal recall the advantage of e-means over k-means depends on the dataset and on how much of the index is read.
- **Faiss main branch** (commit 16a95d6) was tested too: the naive refresh still loses recall there, and the cluster revival introduced after 1.16.0 changes which fixes work.

The current limits are in the README.
