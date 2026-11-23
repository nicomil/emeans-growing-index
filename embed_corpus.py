"""Scarica un corpus con date e ne calcola gli embedding.

  news:  titoli e sommari HuffPost 2012-2022 (heegyu/news-category-dataset)
  arxiv: titolo e abstract di 210.000 articoli arXiv 2007-2021, estratti a caso
         (gfissore/arxiv-abstracts-2021). La data viene dall'identificativo AAMM.numero;
         gli articoli con identificativo del vecchio tipo, precedenti all'aprile 2007, sono esclusi.
  arxiv-full: come arxiv, ma tutti gli articoli (circa 1,9 milioni). Il calcolo procede a blocchi
         e, se interrotto, riparte dall'ultimo blocco finito.

Modelli: "minilm", sentence-transformers/all-MiniLM-L6-v2, 384 dimensioni (predefinito);
"bge", BAAI/bge-base-en-v1.5, 768 dimensioni. Vettori normalizzati; i testi oltre
256 token sono troncati con entrambi. Scrive data/<nome>_embeddings.npy e
data/<nome>_dates.npy, in ordine di data, con nome = corpus per minilm e
corpus-bge per bge.

Uso: uv run --group real embed_corpus.py news|arxiv|arxiv-full [minilm|bge]
"""

import sys
import time
from pathlib import Path

import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

BLOCK = 20_000  # testi per blocco nel calcolo con ripresa


def news():
    rows = load_dataset("heegyu/news-category-dataset", split="train").to_pandas()
    rows["text"] = (rows["headline"].fillna("") + ". " + rows["short_description"].fillna("")).str.strip()
    rows = rows[rows["text"].str.len() > 20].sort_values("date", kind="stable")
    return rows["text"].tolist(), rows["date"].to_numpy().astype("datetime64[D]")


def arxiv(sample=210_000):
    data = load_dataset("gfissore/arxiv-abstracts-2021", split="train").select_columns(["id", "title", "abstract"])
    ids = np.array(data["id"])
    modern = np.flatnonzero(np.char.find(ids, "/") < 0)  # AAMM.numero
    keep = modern if sample is None else np.sort(np.random.default_rng(0).choice(modern, sample, replace=False))
    rows = data.select(keep).to_pandas()
    rows["month"] = rows["id"].str[:4]
    rows["number"] = rows["id"].str[5:].astype(int)
    rows = rows.sort_values(["month", "number"], kind="stable")
    dates = ("20" + rows["month"].str[:2] + "-" + rows["month"].str[2:]).to_numpy().astype("datetime64[M]")
    text = rows["title"].str.replace(r"\s+", " ", regex=True).str.strip() + ". " + rows["abstract"].str.replace(r"\s+", " ", regex=True).str.strip()
    return text.tolist(), dates.astype("datetime64[D]")


if __name__ == "__main__":
    corpus = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else "minilm"
    name = corpus if key == "minilm" else f"{corpus}-{key}"
    texts, dates = {"news": news, "arxiv": arxiv, "arxiv-full": lambda: arxiv(None)}[corpus]()
    assert (dates[1:] >= dates[:-1]).all()
    print(f"{len(texts)} testi dal {dates[0]} al {dates[-1]}; lunghezza mediana {int(np.median([len(t) for t in texts]))} caratteri")
    years, counts = np.unique(dates.astype("datetime64[Y]"), return_counts=True)
    print(", ".join(f"{y}: {c}" for y, c in zip(years, counts)))
    model = SentenceTransformer({"minilm": "sentence-transformers/all-MiniLM-L6-v2", "bge": "BAAI/bge-base-en-v1.5"}[key])
    model.max_seq_length = 256
    Path("data").mkdir(exist_ok=True)
    np.save(f"data/{name}_dates.npy", dates)
    if len(texts) <= BLOCK:
        embeddings = model.encode(texts, batch_size=128, normalize_embeddings=True, show_progress_bar=False)
        np.save(f"data/{name}_embeddings.npy", embeddings.astype(np.float32))
    else:  # a blocchi, su file, con ripresa: un'interruzione costa al più un blocco
        partial, progress = Path(f"data/{name}_embeddings.partial.npy"), Path(f"data/{name}_progress.txt")
        done = int(progress.read_text()) if progress.exists() and partial.exists() else 0
        shape = (len(texts), model.get_sentence_embedding_dimension())
        embeddings = np.lib.format.open_memmap(partial, mode="r+" if done else "w+", dtype=np.float32, shape=shape)
        started = time.time()
        for start in range(done, len(texts), BLOCK):
            block = texts[start : start + BLOCK]
            embeddings[start : start + len(block)] = model.encode(block, batch_size=128, normalize_embeddings=True, show_progress_bar=False)
            embeddings.flush()
            progress.write_text(str(start + len(block)))
            rate = (start + len(block) - done) / (time.time() - started)
            print(f"{start + len(block)} / {len(texts)}, {rate:.0f} testi al secondo", file=sys.stderr, flush=True)
        del embeddings
        partial.rename(f"data/{name}_embeddings.npy")
        progress.unlink()
    print("salvati", len(texts))
