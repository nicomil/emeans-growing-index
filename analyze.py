"""Sintesi dei risultati su dati veri, con intervalli di confidenza.

Legge i risultati interrogazione per interrogazione di exp_real.py e i tempi di
bench_rebuild.py, e scrive results/SINTESI.md.

Intervalli al 95% per ricampionamento delle interrogazioni (2.000 ricampionamenti),
dopo aver mediato sui seed dell'algoritmo. Le differenze tra due strategie sono
appaiate: stesse interrogazioni, stesso ricampionamento. Un intervallo che non
contiene lo zero indica una differenza che non dipende da quali interrogazioni sono
capitate; non dice nulla su altri corpus, e non tiene conto della variabilità tra
seed dell'algoritmo, che è riportata a parte come differenza minima e massima sui
tre seed. I confronti sono molti e non sono corretti per la molteplicità: quelli
vicini allo zero vanno letti come "non distinguibili".

Qui il recall è la media sui seed; nei file exp_real_*.md è la mediana. I due
valori possono differire all'ultima cifra.

Uso: uv run analyze.py > results/SINTESI.md
"""

import json
from pathlib import Path

import numpy as np

from exp_real import BUDGETS, CONTROL, FAISS_NAIVE, ONLINE, REFERENCE, ROUNDS, SEEDS, STALE, TOP, TUNED, ablation_name

DATASETS = {
    "news": "notizie HuffPost, all-MiniLM-L6-v2 (384 dimensioni)",
    "arxiv": "abstract arXiv, all-MiniLM-L6-v2 (384 dimensioni)",
    "news-bge": "notizie HuffPost, bge-base-en-v1.5 (768 dimensioni)",
    "arxiv-bge": "abstract arXiv, bge-base-en-v1.5 (768 dimensioni)",
}
REBUILT = " + liste ricostruite"
NAIVE = ablation_name(False, True, True)
MAIN = [
    STALE, CONTROL, FAISS_NAIVE, FAISS_NAIVE + REBUILT, ONLINE, TUNED, ablation_name(True, False, False),
    "da zero, 1 epoca", "a caldo, 1 epoca a giro", "da zero, 3 epoche", "a caldo, 3 epoche a giro",
    "a caldo con massa a regime, 3 epoche a giro", "a caldo con massa a regime, senza medie finali, 3 epoche a giro", REFERENCE,
]
CONTRASTS = [  # (a, b): si riporta recall(a) - recall(b)
    (REFERENCE, STALE), (CONTROL, STALE), (ONLINE, STALE), (TUNED, ONLINE), (ablation_name(True, False, False), ONLINE),
    ("da zero, 3 epoche", REFERENCE), ("a caldo, 3 epoche a giro", "da zero, 3 epoche"),
    ("a caldo con massa a regime, 3 epoche a giro", "da zero, 3 epoche"),
    ("a caldo con massa a regime, senza medie finali, 3 epoche a giro", "da zero, 3 epoche"),
    ("a caldo, 1 epoca a giro", "da zero, 1 epoca"),
    ("da zero, 1 epoca", STALE), (FAISS_NAIVE + REBUILT, STALE), (FAISS_NAIVE, NAIVE),
]
RESAMPLES = 2000


class Dataset:
    def __init__(self, name):
        self.arrays = np.load(f"results/exp_real_{name}.npz")
        self.runs = json.loads(Path(f"results/exp_real_{name}.json").read_text())

    def per_query(self, strategy, r, budget):
        """Recall di ogni interrogazione, mediato sui seed."""
        return np.mean([self.arrays[f"{seed}|{r}|{strategy}"][budget] for seed in SEEDS], axis=0) / TOP

    def by_seed(self, strategy, r, budget):
        """Recall medio di ogni seed."""
        return np.array([self.arrays[f"{seed}|{r}|{strategy}"][budget].mean() for seed in SEEDS]) / TOP

    def recent(self, r):
        return self.arrays[f"{SEEDS[0]}|{r}|recente"]

    def error(self, strategy, r):
        return np.median([run[strategy][str(r)]["errore"] for run in self.runs])

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
    print(f"Dopo {r} giri, indice da 200.000 testi, {n} interrogazioni. Recall@{TOP}; tra parentesi quadre l'intervallo al 95%.\n")
    recent = data.recent(r)
    recent_picks = np.random.default_rng(1).integers(0, recent.sum(), (RESAMPLES, recent.sum()))
    print(f"Periodo aggiunto: le {recent.sum()} interrogazioni datate dopo l'indice iniziale.\n")
    print("| Strategia | Errore nelle liste | Recall, 1% letto | Recall 1%, periodo aggiunto | Recall, 0,1% letto |")
    print("|---|---|---|---|---|")
    for strategy in MAIN:
        added = "—" if strategy == CONTROL else fmt(*interval(data.per_query(strategy, r, one)[recent], recent_picks))
        print(
            f"| {strategy} | {data.error(strategy, r):+.2f}% | {fmt(*interval(data.per_query(strategy, r, one), picks))} | "
            f"{added} | {fmt(*interval(data.per_query(strategy, r, 0), picks))} |"
        )
    print("\nDifferenze appaiate di recall (1% letto), dopo 10 giri. L'ultima colonna è la stessa differenza calcolata seed per seed.\n")
    print("| Confronto | Differenza [intervallo sulle interrogazioni] | Lo zero è escluso? | Tra i seed [min; max] |")
    print("|---|---|---|---|")
    for a, b in CONTRASTS:
        mean, low, high = interval(data.per_query(a, r, one) - data.per_query(b, r, one), picks)
        seeds = data.by_seed(a, r, one) - data.by_seed(b, r, one)
        print(f"| {a} − {b} | {fmt(mean, low, high, True)} | {'sì' if low > 0 or high < 0 else 'no'} | [{seeds.min():+.3f}; {seeds.max():+.3f}] |")

    print("\nScomposizione dell'uso ingenuo: e-means sui soli testi nuovi, dai centroidi vecchi. Recall con l'1% letto.\n")
    print("| Massa iniziale | Rianimazione | Medie finali | Dopo 1 giro | Dopo 10 giri | Dopo 10 giri, liste ricostruite |")
    print("|---|---|---|---|---|---|")
    first = data.resample(1)
    for mass in (False, True):
        for revival in (True, False):
            for closing in (True, False):
                strategy = ablation_name(mass, revival, closing)
                yes = lambda flag: "sì" if flag else "no"
                print(
                    f"| {yes(mass)} | {yes(revival)} | {yes(closing)} | {fmt(*interval(data.per_query(strategy, 1, one), first))} | "
                    f"{fmt(*interval(data.per_query(strategy, r, one), picks))} | "
                    f"{fmt(*interval(data.per_query(strategy + REBUILT, r, one), picks))} |"
                )
    stale = data.per_query(STALE, r, one).mean()
    print(f"\nPer confronto, dopo 10 giri: mai aggiornare {stale:.3f}; riferimento {data.per_query(REFERENCE, r, one).mean():.3f}.")

    bench = Path(f"results/bench_rebuild_{name}.json")
    if bench.exists():
        records = json.loads(bench.read_text())
        med = lambda method, amount, key: float(np.median([x[key] for x in records if x["metodo"] == method and x["passate"] == amount]))
        amounts = lambda method: sorted({x["passate"] for x in records if x["metodo"] == method})
        print("\nRicalcolo completo, implementazioni di Faiss (mediana di 5 ripetizioni):\n")
        print("| Metodo | Passate | Tempo | Errore di addestramento | Errore sui testi tenuti fuori | Recall, 1% letto |")
        print("|---|---|---|---|---|---|")
        for method in ("e-means", "k-means"):
            for amount in amounts(method):
                print(
                    f"| {method} | {amount} | {med(method, amount, 'secondi'):.1f} s | {med(method, amount, 'errore'):.4f} | "
                    f"{med(method, amount, 'errore fuori'):.4f} | {med(method, amount, 'recall 1.0%'):.3f} |"
                )
        # Quante iterazioni servono al k-means per eguagliare e-means a 3 epoche: si riporta la
        # forchetta tra le due configurazioni misurate, senza interpolare.
        seconds = med("e-means", 3, "secondi")
        for key, label in (("errore", "errore di addestramento"), ("errore fuori", "errore sui testi tenuti fuori")):
            target = med("e-means", 3, key)
            steps = amounts("k-means")
            reached = [a for a in steps if med("k-means", a, key) <= target]
            if not reached:
                print(f"\nA parità di {label}: il k-means non raggiunge e-means a 3 epoche nemmeno con {steps[-1]} iterazioni "
                      f"({med('k-means', steps[-1], 'secondi'):.1f} s contro {seconds:.1f} s): rapporto dei tempi superiore a {med('k-means', steps[-1], 'secondi') / seconds:.1f}.")
            elif reached[0] == steps[0]:
                print(f"\nA parità di {label}: al k-means bastano {steps[0]} iterazioni o meno: rapporto dei tempi al più {med('k-means', steps[0], 'secondi') / seconds:.1f}.")
            else:
                below = steps[steps.index(reached[0]) - 1]
                low, high = med("k-means", below, "secondi"), med("k-means", reached[0], "secondi")
                print(f"\nA parità di {label}: al k-means servono tra {below} e {reached[0]} iterazioni, cioè tra {low:.1f} e {high:.1f} s "
                      f"contro {seconds:.1f} s di e-means a 3 epoche: rapporto dei tempi tra {low / seconds:.1f} e {high / seconds:.1f}.")


if __name__ == "__main__":
    print("# Sintesi dei risultati su dati veri")
    print("\nGenerata da analyze.py. Metodo e limiti nel docstring di analyze.py e di exp_real.py.")
    for name, label in DATASETS.items():
        if Path(f"results/exp_real_{name}.npz").exists():
            report(name, label)
        else:
            print(f"\n## {label}\n\nRisultati mancanti.")
