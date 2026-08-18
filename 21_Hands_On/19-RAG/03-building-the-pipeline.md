# 3. Building the RAG Pipeline (Step by Step)

This walks through building a working RAG pipeline in Python. We'll use:
- `pypdf` / plain text loaders for ingestion
- A recursive text splitter for chunking
- OpenAI-compatible embeddings (swap in any provider)
- `pgvector` (Postgres) as the vector store — since most backends already have Postgres

You can substitute Chroma or Qdrant if you don't want to touch Postgres; the logic is the same, only the storage client differs.

## 3.0 Install dependencies

```bash
pip install psycopg[binary] pgvector openai pypdf tiktoken --break-system-packages
```

Enable the extension once in your Postgres database:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 3.1 Define the schema

```sql
CREATE TABLE documents (
    id          BIGSERIAL PRIMARY KEY,
    source      TEXT NOT NULL,          -- e.g. filename or URL
    chunk_index INT NOT NULL,
    content     TEXT NOT NULL,
    embedding   VECTOR(1536) NOT NULL,  -- dimension must match your embedding model
    metadata    JSONB DEFAULT '{}'::jsonb,
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- Approximate nearest neighbor index (IVFFlat or HNSW)
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

## 3.2 Ingestion: load raw documents

```python
# ingest/load.py
from pypdf import PdfReader
from pathlib import Path

def load_text_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def load_document(path: str) -> str:
    if path.endswith(".pdf"):
        return load_pdf(path)
    return load_text_file(path)
```

## 3.3 Chunking

```python
# ingest/chunk.py
import tiktoken

encoder = tiktoken.get_encoding("cl100k_base")

def split_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """Token-aware recursive-ish splitter with overlap."""
    tokens = encoder.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunks.append(encoder.decode(chunk_tokens))
        if end == len(tokens):
            break
        start = end - overlap  # step forward, keeping overlap
    return chunks
```

For structure-aware splitting (markdown, code), split on headers/functions first, then apply `split_text` to any oversized sections.

## 3.4 Embedding

```python
# ingest/embed.py
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from env

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [item.embedding for item in response.data]
```

> Swap this function's internals to call Voyage, Cohere, or a local `sentence-transformers` model — everything downstream just expects a list of float vectors.

## 3.5 Storing embeddings

```python
# ingest/store.py
import psycopg
from pgvector.psycopg import register_vector

def get_connection(dsn: str):
    conn = psycopg.connect(dsn, autocommit=True)
    register_vector(conn)
    return conn

def store_chunks(conn, source: str, chunks: list[str], embeddings: list[list[float]], metadata: dict = None):
    with conn.cursor() as cur:
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            cur.execute(
                """
                INSERT INTO documents (source, chunk_index, content, embedding, metadata)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (source, i, chunk, emb, metadata or {}),
            )
```

## 3.6 Full ingestion script

```python
# ingest/run.py
from ingest.load import load_document
from ingest.chunk import split_text
from ingest.embed import embed_texts
from ingest.store import get_connection, store_chunks
import os

def ingest_file(path: str, dsn: str):
    text = load_document(path)
    chunks = split_text(text, chunk_size=500, overlap=50)
    embeddings = embed_texts(chunks)

    conn = get_connection(dsn)
    store_chunks(conn, source=os.path.basename(path), chunks=chunks, embeddings=embeddings)
    print(f"Ingested {len(chunks)} chunks from {path}")

if __name__ == "__main__":
    ingest_file("docs/employee_handbook.pdf", dsn=os.environ["DATABASE_URL"])
```

Run it for every document in your corpus (loop over a folder, or trigger on upload — see file 4 for the API-driven version).

## 3.7 Retrieval

```python
# retrieve/search.py
from ingest.embed import embed_texts

def search(conn, query: str, top_k: int = 5, filters: dict = None) -> list[dict]:
    query_embedding = embed_texts([query])[0]

    sql = """
        SELECT source, chunk_index, content, metadata,
               1 - (embedding <=> %s) AS similarity
        FROM documents
        ORDER BY embedding <=> %s
        LIMIT %s
    """
    with conn.cursor() as cur:
        cur.execute(sql, (query_embedding, query_embedding, top_k))
        rows = cur.fetchall()

    return [
        {"source": r[0], "chunk_index": r[1], "content": r[2], "metadata": r[3], "similarity": r[4]}
        for r in rows
    ]
```

`<=>` is pgvector's cosine distance operator; `1 - distance` gives you a similarity score in [0, 1] (roughly).

## 3.8 Prompt assembly + generation

```python
# generate/answer.py
from anthropic import Anthropic

client = Anthropic()  # reads ANTHROPIC_API_KEY from env

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using ONLY the
provided context. If the answer is not contained in the context, say you don't know.
Always cite sources using the [n] markers matching the context blocks."""

def build_context_block(results: list[dict]) -> str:
    blocks = []
    for i, r in enumerate(results, start=1):
        blocks.append(f"[{i}] (source: {r['source']})\n{r['content']}")
    return "\n\n".join(blocks)

def answer_question(query: str, results: list[dict]) -> str:
    context = build_context_block(results)
    user_message = f"Context:\n{context}\n\nQuestion: {query}"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text
```

## 3.9 Putting it all together

```python
# rag.py
def rag_query(conn, query: str, top_k: int = 5) -> dict:
    results = search(conn, query, top_k=top_k)
    answer = answer_question(query, results)
    return {
        "answer": answer,
        "sources": [{"source": r["source"], "similarity": r["similarity"]} for r in results],
    }
```

That's a complete, working RAG pipeline: ingest → chunk → embed → store → retrieve → generate.

Next: [`04-backend-integration.md`](04-backend-integration.md) — wrapping this in a real backend API with FastAPI, including upload endpoints, async processing, and streaming responses.
