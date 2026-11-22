"""Scarica un corpus con date e ne calcola gli embedding.

  news:  titoli e sommari HuffPost 2012-2022 (heegyu/news-category-dataset)
  arxiv: titolo e abstract di 210.000 articoli arXiv 2007-2021, estratti a caso
         (gfissore/arxiv-abstracts-2021). La data viene dall'identificativo AAMM.numero;
         gli articoli con identificativo del vecchio tipo, precedenti all'aprile 2007, sono esclusi.

Modello: sentence-transformers/all-MiniLM-L6-v2, 384 dimensioni, vettori normalizzati;
i testi oltre 256 token sono troncati. Scrive data/<corpus>_embeddings.npy e
data/<corpus>_dates.npy, in ordine di data.

Uso: uv run --group real embed_corpus.py news|arxiv
"""

import sys
from pathlib import Path

import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer


def news():
    rows = load_dataset("heegyu/news-category-dataset", split="train").to_pandas()
    rows["text"] = (rows["headline"].fillna("") + ". " + rows["short_description"].fillna("")).str.strip()
    rows = rows[rows["text"].str.len() > 20].sort_values("date", kind="stable")
    return rows["text"].tolist(), rows["date"].to_numpy().astype("datetime64[D]")


def arxiv():
    data = load_dataset("gfissore/arxiv-abstracts-2021", split="train").select_columns(["id", "title", "abstract"])
    ids = np.array(data["id"])
    modern = np.flatnonzero(np.char.find(ids, "/") < 0)  # AAMM.numero
    keep = np.sort(np.random.default_rng(0).choice(modern, 210_000, replace=False))
    rows = data.select(keep).to_pandas()
    rows["month"] = rows["id"].str[:4]
    rows["number"] = rows["id"].str[5:].astype(int)
    rows = rows.sort_values(["month", "number"], kind="stable")
    dates = ("20" + rows["month"].str[:2] + "-" + rows["month"].str[2:]).to_numpy().astype("datetime64[M]")
    text = rows["title"].str.replace(r"\s+", " ", regex=True).str.strip() + ". " + rows["abstract"].str.replace(r"\s+", " ", regex=True).str.strip()
    return text.tolist(), dates.astype("datetime64[D]")


if __name__ == "__main__":
    corpus = sys.argv[1]
    texts, dates = {"news": news, "arxiv": arxiv}[corpus]()
    assert (dates[1:] >= dates[:-1]).all()
    print(f"{len(texts)} testi dal {dates[0]} al {dates[-1]}; lunghezza mediana {int(np.median([len(t) for t in texts]))} caratteri")
    years, counts = np.unique(dates.astype("datetime64[Y]"), return_counts=True)
    print(", ".join(f"{y}: {c}" for y, c in zip(years, counts)))
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(texts, batch_size=128, normalize_embeddings=True, show_progress_bar=False)
    Path("data").mkdir(exist_ok=True)
    np.save(f"data/{corpus}_embeddings.npy", embeddings.astype(np.float32))
    np.save(f"data/{corpus}_dates.npy", dates)
    print("salvati", embeddings.shape)
