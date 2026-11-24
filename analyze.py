"""Summary of the results on real data, with confidence intervals.

Reads the query-by-query results of exp_real.py and the timings of
bench_rebuild.py, and writes results/SUMMARY.md.

95% intervals by resampling the queries (2,000 resamples), after averaging over
the algorithm seeds. The differences between two strategies are paired: same
queries, same resampling. An interval that does not contain zero indicates a
difference that does not depend on which queries happened to be drawn; it says
nothing about other corpora, and it does not account for the variability between
algorithm seeds, which is reported separately as the minimum and maximum difference
over the three seeds. The comparisons are many and are not corrected for
multiplicity: those close to zero should be read as "not distinguishable".

Here the recall is the mean over the seeds; in the exp_real_*.md files it is the
median. The two values can differ in the last digit.

Usage: uv run analyze.py > results/SUMMARY.md
"""

import json
from pathlib import Path

import numpy as np

from exp_real import BUDGETS, CONTROL, FAISS_NAIVE, ONLINE, REFERENCE, ROUNDS, SEEDS, STALE, TOP, TUNED, ablation_name

DATASETS = {
    "news": "HuffPost news, all-MiniLM-L6-v2 (384 dimensions)",
    "arxiv": "arXiv abstracts, all-MiniLM-L6-v2 (384 dimensions)",
    "news-bge": "HuffPost news, bge-base-en-v1.5 (768 dimensions)",
    "arxiv-bge": "arXiv abstracts, bge-base-en-v1.5 (768 dimensions)",
}
REBUILT = " + lists rebuilt"
NAIVE = ablation_name(False, True, True)
MAIN = [
    STALE, CONTROL, FAISS_NAIVE, FAISS_NAIVE + REBUILT, ONLINE, TUNED, ablation_name(True, False, False),
    "from scratch, 1 epoch", "warm start, 1 epoch per round", "from scratch, 3 epochs", "warm start, 3 epochs per round",
    "warm start with steady-state mass, 3 epochs per round", "warm start with steady-state mass, no final means, 3 epochs per round", REFERENCE,
]
CONTRASTS = [  # (a, b): recall(a) - recall(b) is reported
    (REFERENCE, STALE), (CONTROL, STALE), (ONLINE, STALE), (TUNED, ONLINE), (ablation_name(True, False, False), ONLINE),
    ("from scratch, 3 epochs", REFERENCE), ("warm start, 3 epochs per round", "from scratch, 3 epochs"),
    ("warm start with steady-state mass, 3 epochs per round", "from scratch, 3 epochs"),
    ("warm start with steady-state mass, no final means, 3 epochs per round", "from scratch, 3 epochs"),
    ("warm start, 1 epoch per round", "from scratch, 1 epoch"),
    ("from scratch, 1 epoch", STALE), (FAISS_NAIVE + REBUILT, STALE), (FAISS_NAIVE, NAIVE),
]
RESAMPLES = 2000


class Dataset:
    def __init__(self, name):
        self.arrays = np.load(f"results/exp_real_{name}.npz")
        self.runs = json.loads(Path(f"results/exp_real_{name}.json").read_text())

    def per_query(self, strategy, r, budget):
        """Recall of every query, averaged over the seeds."""
        return np.mean([self.arrays[f"{seed}|{r}|{strategy}"][budget] for seed in SEEDS], axis=0) / TOP

    def by_seed(self, strategy, r, budget):
        """Mean recall of every seed."""
        return np.array([self.arrays[f"{seed}|{r}|{strategy}"][budget].mean() for seed in SEEDS]) / TOP

    def recent(self, r):
        return self.arrays[f"{SEEDS[0]}|{r}|recent"]

    def error(self, strategy, r):
        return np.median([run[strategy][str(r)]["error"] for run in self.runs])

    def resample(self, r):
        n = self.arrays[f"{SEEDS[0]}|{r}|{REFERENCE}"].shape[1]
        return np.random.default_rng(0).integers(0, n, (RESAMPLES, n))


def interval(values, picks):
    means = values[picks].mean(1)
    return values.mean(), np.percentile(means, 2.5), np.percentile(means, 97.5)


def fmt(mean, low, high, signed=False):
    sign = "+" if signed else ""
    return f"{mean:{sign}.3f} [{low:{sign}.3f}; {high:{sign}.3f}]"


def report(name, label):
    data = Dataset(name)
    r, one = ROUNDS, len(BUDGETS) - 1
    picks = data.resample(r)
    n = picks.shape[1]
    print(f"\n## {label}\n")
    print(f"After {r} rounds, index of 200,000 texts, {n} queries. Recall@{TOP}; in square brackets the 95% interval.\n")
    recent = data.recent(r)
    recent_picks = np.random.default_rng(1).integers(0, recent.sum(), (RESAMPLES, recent.sum()))
    print(f"Added period: the {recent.sum()} queries dated after the initial index.\n")
    print("| Strategy | Error in the lists | Recall, 1% read | Recall 1%, added period | Recall, 0.1% read |")
    print("|---|---|---|---|---|")
    for strategy in MAIN:
        added = "—" if strategy == CONTROL else fmt(*interval(data.per_query(strategy, r, one)[recent], recent_picks))
        print(
            f"| {strategy} | {data.error(strategy, r):+.2f}% | {fmt(*interval(data.per_query(strategy, r, one), picks))} | "
            f"{added} | {fmt(*interval(data.per_query(strategy, r, 0), picks))} |"
        )
    print("\nPaired differences in recall (1% read), after 10 rounds. The last column is the same difference computed seed by seed.\n")
    print("| Comparison | Difference [interval over the queries] | Is zero excluded? | Across seeds [min; max] |")
    print("|---|---|---|---|")
    for a, b in CONTRASTS:
        mean, low, high = interval(data.per_query(a, r, one) - data.per_query(b, r, one), picks)
        seeds = data.by_seed(a, r, one) - data.by_seed(b, r, one)
        print(f"| {a} − {b} | {fmt(mean, low, high, True)} | {'yes' if low > 0 or high < 0 else 'no'} | [{seeds.min():+.3f}; {seeds.max():+.3f}] |")

    print("\nBreakdown of the naive use: e-means on the new texts only, from the old centroids. Recall with 1% read.\n")
    print("| Initial mass | Revival | Final means | After 1 round | After 10 rounds | After 10 rounds, lists rebuilt |")
    print("|---|---|---|---|---|---|")
    first = data.resample(1)
    for mass in (False, True):
        for revival in (True, False):
            for closing in (True, False):
                strategy = ablation_name(mass, revival, closing)
                yes = lambda flag: "yes" if flag else "no"
                print(
                    f"| {yes(mass)} | {yes(revival)} | {yes(closing)} | {fmt(*interval(data.per_query(strategy, 1, one), first))} | "
                    f"{fmt(*interval(data.per_query(strategy, r, one), picks))} | "
                    f"{fmt(*interval(data.per_query(strategy + REBUILT, r, one), picks))} |"
                )
    stale = data.per_query(STALE, r, one).mean()
    print(f"\nFor comparison, after 10 rounds: never update {stale:.3f}; reference {data.per_query(REFERENCE, r, one).mean():.3f}.")

    bench = Path(f"results/bench_rebuild_{name}.json")
    if bench.exists():
        records = json.loads(bench.read_text())
        med = lambda method, amount, key: float(np.median([x[key] for x in records if x["method"] == method and x["passes"] == amount]))
        amounts = lambda method: sorted({x["passes"] for x in records if x["method"] == method})
        print("\nTraining of the centroids on the 200,000 texts, Faiss implementations (median of 6 repetitions; the reassignment of the vectors is not included in the time):\n")
        print("| Method | Passes | Time | Training error | Error on the held-out texts | Recall, 1% read |")
        print("|---|---|---|---|---|---|")
        for method in ("e-means", "k-means"):
            for amount in amounts(method):
                print(
                    f"| {method} | {amount} | {med(method, amount, 'seconds'):.1f} s | {med(method, amount, 'error'):.4f} | "
                    f"{med(method, amount, 'held-out error'):.4f} | {med(method, amount, 'recall 1.0%'):.3f} |"
                )
        # How many iterations k-means needs to match e-means at 3 epochs: the bracket between
        # the two measured configurations is reported, without interpolating.
        seconds = med("e-means", 3, "seconds")
        # The recall is rounded to the third digit: on about 2,900 queries the uncertainty is a few thousandths.
        for key, label, better in (
            ("error", "training error", -1), ("held-out error", "error on the held-out texts", -1),
            ("recall 0.1%", "recall with 0.1% of the index read", 1), ("recall 1.0%", "recall with 1% of the index read", 1),
        ):
            target = round(med("e-means", 3, key), 3) if better > 0 else med("e-means", 3, key)
            steps = amounts("k-means")
            value = lambda a: round(med("k-means", a, key), 3) if better > 0 else med("k-means", a, key)
            reached = [a for a in steps if better * (value(a) - target) >= 0]
            if not reached:
                print(f"\nAt equal {label}: k-means does not reach e-means at 3 epochs even with {steps[-1]} iterations "
                      f"({med('k-means', steps[-1], 'seconds'):.1f} s against {seconds:.1f} s): time ratio above {med('k-means', steps[-1], 'seconds') / seconds:.1f}.")
            elif reached[0] == steps[0]:
                print(f"\nAt equal {label}: k-means needs {steps[0]} iterations or fewer: time ratio at most {med('k-means', steps[0], 'seconds') / seconds:.1f}.")
            else:
                below = steps[steps.index(reached[0]) - 1]
                low, high = med("k-means", below, "seconds"), med("k-means", reached[0], "seconds")
                print(f"\nAt equal {label}: k-means needs between {below} and {reached[0]} iterations, i.e. between {low:.1f} and {high:.1f} s "
                      f"against {seconds:.1f} s for e-means at 3 epochs: time ratio between {low / seconds:.1f} and {high / seconds:.1f}.")


if __name__ == "__main__":
    print("# Summary of the results on real data")
    print("\nGenerated by analyze.py. Method and limits in the docstrings of analyze.py and exp_real.py.")
    for name, label in DATASETS.items():
        if Path(f"results/exp_real_{name}.npz").exists():
            report(name, label)
        else:
            print(f"\n## {label}\n\nResults missing.")
