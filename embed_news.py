"""Scarica i titoli HuffPost 2012-2022 e ne calcola gli embedding.

Corpus: heegyu/news-category-dataset su Hugging Face (titolo, sommario, data).
Modello: sentence-transformers/all-MiniLM-L6-v2, 384 dimensioni, vettori normalizzati.
Scrive data/news_embeddings.npy e data/news_dates.npy, in ordine di data.

Uso: uv run --group real embed_news.py
"""

from pathlib import Path

import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

rows = load_dataset("heegyu/news-category-dataset", split="train").to_pandas()
rows["text"] = (rows["headline"].fillna("") + ". " + rows["short_description"].fillna("")).str.strip()
rows = rows[rows["text"].str.len() > 20].sort_values("date", kind="stable")
print(f"{len(rows)} articoli dal {rows['date'].min():%Y-%m-%d} al {rows['date'].max():%Y-%m-%d}")
print(rows["date"].dt.year.value_counts().sort_index().to_string())

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(rows["text"].tolist(), batch_size=256, normalize_embeddings=True, show_progress_bar=False)
Path("data").mkdir(exist_ok=True)
np.save("data/news_embeddings.npy", embeddings.astype(np.float32))
np.save("data/news_dates.npy", rows["date"].to_numpy().astype("datetime64[D]"))
print("salvati", embeddings.shape)
