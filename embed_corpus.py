"""Downloads a dated corpus and computes its embeddings.

  news:  HuffPost headlines and summaries 2012-2022 (heegyu/news-category-dataset)
  arxiv: title and abstract of 210,000 arXiv papers 2007-2021, drawn at random
         (gfissore/arxiv-abstracts-2021). The date comes from the YYMM.number identifier;
         papers with an old-style identifier, earlier than April 2007, are excluded.
  msmarco: 1,600,000 MS MARCO passages drawn at random and put in random order (BeIR/msmarco).
         They have no date: they serve as an archive without drift. Along with them the vectors of
         3,000 real user questions are computed, in data/msmarco_queries.npy.
  stackoverflow: 1,600,000 Stack Overflow answers drawn at random among all those posted from 2008
         to June 2023, in date order (mikex86/stackoverflow-posts, content under CC BY-SA). Along with
         them, the titles of 3,000 questions drawn at random, with their dates: real user questions on
         an archive with real drift, in data/stackoverflow_queries.npy and _query_dates.npy.
  arxiv-full: like arxiv, but all the papers (about 1.9 million). The computation proceeds in blocks
         and, if interrupted, restarts from the last finished block.

Models: "minilm", sentence-transformers/all-MiniLM-L6-v2, 384 dimensions (default);
"bge", BAAI/bge-base-en-v1.5, 768 dimensions. Normalised vectors; texts longer than
256 tokens are truncated with both. Writes data/<name>_embeddings.npy and
data/<name>_dates.npy, in date order, with name = corpus for minilm and
corpus-bge for bge.

Usage: uv run --group real embed_corpus.py news|arxiv|arxiv-full|msmarco|stackoverflow [minilm|bge]
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


def stackoverflow(sample=1_600_000, n_queries=3_000, shards=59):
    """Returns answers and dates, plus question titles and their dates.

    Reads one 400-600 MB file at a time, keeps a random 5.5% of the answers and 0.05% of the questions
    in data/so_parts/, and deletes the download: an interruption costs at most one file.
    """
    import pandas as pd
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download

    parts = Path("data/so_parts")
    parts.mkdir(parents=True, exist_ok=True)
    for i in range(shards):
        part = parts / f"{i:05d}.parquet"
        if part.exists():
            continue
        name = f"stackoverflow-posts-{i:05d}-of-{shards - 1:05d}.parquet"
        for attempt in range(5):
            try:
                path = hf_hub_download("mikex86/stackoverflow-posts", name, repo_type="dataset", local_dir="data/so_download")
                break
            except Exception as error:  # network hiccups over a 34 GB download
                print(f"{name}: {error!r}, retry {attempt + 1}", file=sys.stderr, flush=True)
                time.sleep(60)
        else:
            raise RuntimeError(f"cannot download {name}")
        rows = pq.read_table(path, columns=["PostTypeId", "Body", "Title", "CreationDate"]).to_pandas()
        draw = np.random.default_rng(i).random(len(rows))
        answer = (rows["PostTypeId"] == 2) & (rows["Body"].str.len() > 50) & (draw < 0.055)
        question = (rows["PostTypeId"] == 1) & (rows["Title"].str.len() > 15) & (draw < 0.0005)
        rows[answer | question].to_parquet(part.with_suffix(".tmp"))
        part.with_suffix(".tmp").rename(part)
        Path(path).unlink()
        print(f"{name}: {int(answer.sum())} answers, {int(question.sum())} questions kept", file=sys.stderr, flush=True)
    rows = pd.concat([pd.read_parquet(parts / f"{i:05d}.parquet") for i in range(shards)], ignore_index=True)
    rows["date"] = rows["CreationDate"].str[:10].to_numpy().astype("datetime64[D]")
    answers = rows[rows["PostTypeId"] == 2]
    answers = answers.iloc[np.sort(np.random.default_rng(0).choice(len(answers), sample, replace=False))].sort_values("CreationDate", kind="stable")
    questions = rows[rows["PostTypeId"] == 1]
    questions = questions.iloc[np.random.default_rng(1).choice(len(questions), n_queries, replace=False)]
    clean = lambda text: text.str.replace(r"\s+", " ", regex=True).str.strip()
    return clean(answers["Body"]).tolist(), answers["date"].to_numpy(), clean(questions["Title"]).tolist(), questions["date"].to_numpy()


if __name__ == "__main__":
    corpus = sys.argv[1]
    key = sys.argv[2] if len(sys.argv) > 2 else "minilm"
    name = corpus if key == "minilm" else f"{corpus}-{key}"
    texts, dates, *asked = {"news": news, "arxiv": arxiv, "arxiv-full": lambda: arxiv(None), "msmarco": msmarco, "stackoverflow": stackoverflow}[corpus]()
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
    if asked:  # real questions with their own dates
        np.save(f"data/{name}_queries.npy", model.encode(asked[0], batch_size=128, normalize_embeddings=True, show_progress_bar=False).astype(np.float32))
        np.save(f"data/{name}_query_dates.npy", asked[1])
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
