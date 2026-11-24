"""Downloads a dated corpus and computes its embeddings.

  news:  HuffPost headlines and summaries 2012-2022 (heegyu/news-category-dataset)
  arxiv: title and abstract of 210,000 arXiv papers 2007-2021, drawn at random
         (gfissore/arxiv-abstracts-2021). The date comes from the YYMM.number identifier;
         papers with an old-style identifier, earlier than April 2007, are excluded.
  msmarco: 1,600,000 MS MARCO passages drawn at random and put in random order (BeIR/msmarco).
         They have no date: they serve as an archive without drift. Along with them the vectors of
         3,000 real user questions are computed, in data/msmarco_queries.npy.
  arxiv-full: like arxiv, but all the papers (about 1.9 million). The computation proceeds in blocks
         and, if interrupted, restarts from the last finished block.

Models: "minilm", sentence-transformers/all-MiniLM-L6-v2, 384 dimensions (default);
"bge", BAAI/bge-base-en-v1.5, 768 dimensions. Normalised vectors; texts longer than
256 tokens are truncated with both. Writes data/<name>_embeddings.npy and
data/<name>_dates.npy, in date order, with name = corpus for minilm and
corpus-bge for bge.

Usage: uv run --group real embed_corpus.py news|arxiv|arxiv-full|msmarco [minilm|bge]
"""

import sys
import time
from pathlib import Path

import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

BLOCK = 20_000  # texts per block in the resumable computation


def news():
    rows = load_dataset("heegyu/news-category-dataset", split="train").to_pandas()
    rows["text"] = (rows["headline"].fillna("") + ". " + rows["short_description"].fillna("")).str.strip()
    rows = rows[rows["text"].str.len() > 20].sort_values("date", kind="stable")
    return rows["text"].tolist(), rows["date"].to_numpy().astype("datetime64[D]")


def arxiv(sample=210_000):
    data = load_dataset("gfissore/arxiv-abstracts-2021", split="train").select_columns(["id", "title", "abstract"])
    ids = np.array(data["id"])
    modern = np.flatnonzero(np.char.find(ids, "/") < 0)  # YYMM.number
    keep = modern if sample is None else np.sort(np.random.default_rng(0).choice(modern, sample, replace=False))
    rows = data.select(keep).to_pandas()
    rows["month"] = rows["id"].str[:4]
    rows["number"] = rows["id"].str[5:].astype(int)
    rows = rows.sort_values(["month", "number"], kind="stable")
    dates = ("20" + rows["month"].str[:2] + "-" + rows["month"].str[2:]).to_numpy().astype("datetime64[M]")
    text = rows["title"].str.replace(r"\s+", " ", regex=True).str.strip() + ". " + rows["abstract"].str.replace(r"\s+", " ", regex=True).str.strip()
    return text.tolist(), dates.astype("datetime64[D]")


def msmarco(sample=1_600_000):
    data = load_dataset("BeIR/msmarco", "corpus", split="corpus")
    keep = np.sort(np.random.default_rng(0).choice(len(data), sample, replace=False))
    text = data.select(keep).to_pandas()["text"].str.replace(r"\s+", " ", regex=True).str.strip()
    text = text.iloc[np.random.default_rng(1).permutation(len(text))]
    return text.tolist(), np.full(len(text), np.datetime64("2018-01-01", "D"))


if __name__ == "__main__":
    corpus = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else "minilm"
    name = corpus if key == "minilm" else f"{corpus}-{key}"
    texts, dates = {"news": news, "arxiv": arxiv, "arxiv-full": lambda: arxiv(None), "msmarco": msmarco}[corpus]()
    assert (dates[1:] >= dates[:-1]).all()
    print(f"{len(texts)} texts from {dates[0]} to {dates[-1]}; median length {int(np.median([len(t) for t in texts]))} characters")
    years, counts = np.unique(dates.astype("datetime64[Y]"), return_counts=True)
    print(", ".join(f"{y}: {c}" for y, c in zip(years, counts)))
    model = SentenceTransformer({"minilm": "sentence-transformers/all-MiniLM-L6-v2", "bge": "BAAI/bge-base-en-v1.5"}[key])
    model.max_seq_length = 256
    Path("data").mkdir(exist_ok=True)
    np.save(f"data/{name}_dates.npy", dates)
    if corpus == "msmarco":
        asked = load_dataset("BeIR/msmarco", "queries", split="queries")
        asked = asked.select(np.sort(np.random.default_rng(0).choice(len(asked), 3_000, replace=False)))["text"]
        np.save(f"data/{name}_queries.npy", model.encode(asked, batch_size=128, normalize_embeddings=True, show_progress_bar=False).astype(np.float32))
    if len(texts) <= BLOCK:
        embeddings = model.encode(texts, batch_size=128, normalize_embeddings=True, show_progress_bar=False)
        np.save(f"data/{name}_embeddings.npy", embeddings.astype(np.float32))
    else:  # in blocks, on file, resumable: an interruption costs at most one block
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
            print(f"{start + len(block)} / {len(texts)}, {rate:.0f} texts per second", file=sys.stderr, flush=True)
        del embeddings
        partial.rename(f"data/{name}_embeddings.npy")
        progress.unlink()
    print("saved", len(texts))
