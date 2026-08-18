# 4. Integrating RAG into a Backend Application

This shows a complete, realistic **FastAPI** backend that exposes RAG over HTTP:

- `POST /documents` — upload and ingest a document
- `POST /query` — ask a question, get a grounded answer with sources
- `POST /query/stream` — same, but streamed token-by-token
- Background processing so uploads don't block the request
- Basic multi-tenancy via metadata filtering

The same pattern works with Express/Node, Django, Go, etc. — only the syntax changes, the architecture doesn't.

## 4.1 Project structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app + routes
│   ├── config.py            # env/config
│   ├── db.py                # Postgres connection pool
│   ├── ingest.py            # load/chunk/embed/store (from file 3)
│   ├── retrieve.py          # vector search
│   ├── generate.py          # prompt assembly + LLM call
│   └── schemas.py           # Pydantic request/response models
├── requirements.txt
└── .env
```

## 4.2 Config

```python
# app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.environ["DATABASE_URL"]
    openai_api_key: str = os.environ["OPENAI_API_KEY"]
    anthropic_api_key: str = os.environ["ANTHROPIC_API_KEY"]
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "claude-sonnet-4-6"
    top_k: int = 5

settings = Settings()
```

## 4.3 Connection pool

```python
# app/db.py
from psycopg_pool import ConnectionPool
from pgvector.psycopg import register_vector
from app.config import settings

def configure(conn):
    register_vector(conn)

pool = ConnectionPool(conninfo=settings.database_url, configure=configure, min_size=2, max_size=10)
```

Using a pool (instead of one connection per request) matters once you have concurrent traffic — don't skip this in production.

## 4.4 Request/response schemas

```python
# app/schemas.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str
    tenant_id: str | None = None
    top_k: int = 5

class Source(BaseModel):
    source: str
    similarity: float

class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]

class IngestResponse(BaseModel):
    document_id: str
    status: str
    chunk_count: int | None = None
```

## 4.5 The FastAPI app

```python
# app/main.py
import uuid
from fastapi import FastAPI, UploadFile, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from app.db import pool
from app.schemas import QueryRequest, QueryResponse, IngestResponse
from app.ingest import ingest_bytes
from app.retrieve import search
from app.generate import answer_question, stream_answer

app = FastAPI(title="RAG API")

# In-memory job status for demo purposes — use Redis/DB in production
JOBS: dict[str, dict] = {}


@app.post("/documents", response_model=IngestResponse)
async def upload_document(file: UploadFile, background_tasks: BackgroundTasks, tenant_id: str = "default"):
    doc_id = str(uuid.uuid4())
    content = await file.read()
    JOBS[doc_id] = {"status": "processing"}

    background_tasks.add_task(process_document, doc_id, file.filename, content, tenant_id)

    return IngestResponse(document_id=doc_id, status="processing")


def process_document(doc_id: str, filename: str, content: bytes, tenant_id: str):
    try:
        chunk_count = ingest_bytes(pool, filename, content, metadata={"tenant_id": tenant_id})
        JOBS[doc_id] = {"status": "complete", "chunk_count": chunk_count}
    except Exception as e:
        JOBS[doc_id] = {"status": "failed", "error": str(e)}


@app.get("/documents/{doc_id}")
def get_document_status(doc_id: str):
    job = JOBS.get(doc_id)
    if not job:
        raise HTTPException(status_code=404, detail="Unknown document id")
    return job


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    with pool.connection() as conn:
        results = search(conn, req.question, top_k=req.top_k, tenant_id=req.tenant_id)

    if not results:
        return QueryResponse(answer="I don't have information on that.", sources=[])

    answer = answer_question(req.question, results)
    sources = [{"source": r["source"], "similarity": r["similarity"]} for r in results]
    return QueryResponse(answer=answer, sources=sources)


@app.post("/query/stream")
def query_stream(req: QueryRequest):
    with pool.connection() as conn:
        results = search(conn, req.question, top_k=req.top_k, tenant_id=req.tenant_id)

    def event_generator():
        for token in stream_answer(req.question, results):
            yield token

    return StreamingResponse(event_generator(), media_type="text/plain")
```

## 4.6 Ingestion adapted for uploaded bytes

```python
# app/ingest.py (extends file 3's ingest logic)
import io
from pypdf import PdfReader
from app.chunking import split_text
from app.embedding import embed_texts

def extract_text(filename: str, content: bytes) -> str:
    if filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    return content.decode("utf-8", errors="ignore")

def ingest_bytes(pool, filename: str, content: bytes, metadata: dict) -> int:
    text = extract_text(filename, content)
    chunks = split_text(text, chunk_size=500, overlap=50)
    embeddings = embed_texts(chunks)

    with pool.connection() as conn:
        with conn.cursor() as cur:
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                cur.execute(
                    """
                    INSERT INTO documents (source, chunk_index, content, embedding, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (filename, i, chunk, emb, metadata),
                )
    return len(chunks)
```

## 4.7 Retrieval with tenant filtering

Multi-tenant apps must never let one tenant's query retrieve another tenant's data. Filter at the SQL level, not in application code:

```python
# app/retrieve.py
from app.embedding import embed_texts

def search(conn, query: str, top_k: int = 5, tenant_id: str | None = None) -> list[dict]:
    query_embedding = embed_texts([query])[0]

    if tenant_id:
        sql = """
            SELECT source, content, metadata, 1 - (embedding <=> %s) AS similarity
            FROM documents
            WHERE metadata->>'tenant_id' = %s
            ORDER BY embedding <=> %s
            LIMIT %s
        """
        params = (query_embedding, tenant_id, query_embedding, top_k)
    else:
        sql = """
            SELECT source, content, metadata, 1 - (embedding <=> %s) AS similarity
            FROM documents
            ORDER BY embedding <=> %s
            LIMIT %s
        """
        params = (query_embedding, query_embedding, top_k)

    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    return [{"source": r[0], "content": r[1], "metadata": r[2], "similarity": r[3]} for r in rows]
```

## 4.8 Streaming generation

```python
# app/generate.py
from anthropic import Anthropic
from app.config import settings

client = Anthropic(api_key=settings.anthropic_api_key)

SYSTEM_PROMPT = """Answer using ONLY the provided context. If the answer isn't there, say you don't know.
Cite sources using [n] markers."""

def build_context(results: list[dict]) -> str:
    return "\n\n".join(f"[{i}] (source: {r['source']})\n{r['content']}" for i, r in enumerate(results, 1))

def answer_question(query: str, results: list[dict]) -> str:
    context = build_context(results)
    response = client.messages.create(
        model=settings.chat_model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}],
    )
    return response.content[0].text

def stream_answer(query: str, results: list[dict]):
    context = build_context(results)
    with client.messages.stream(
        model=settings.chat_model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}],
    ) as stream:
        for text in stream.text_stream:
            yield text
```

## 4.9 Calling it from a client

```bash
# Upload a document
curl -X POST http://localhost:8000/documents \
  -F "file=@handbook.pdf" \
  -F "tenant_id=acme-corp"

# Ask a question
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many leave days carry over?", "tenant_id": "acme-corp"}'
```

Response:
```json
{
  "answer": "Up to 5 unused leave days carry over to the next year [2].",
  "sources": [
    {"source": "handbook.pdf", "similarity": 0.87},
    {"source": "handbook.pdf", "similarity": 0.81}
  ]
}
```

## 4.10 Where this fits in a larger app

- **Auth**: put standard auth middleware (JWT/session) in front of every route; derive `tenant_id`/`user_id` from the authenticated session rather than trusting a request body field in production.
- **Rate limiting**: LLM and embedding calls cost money per request — rate-limit `/query` per user/tenant.
- **Async ingestion at scale**: swap `BackgroundTasks` for a real task queue (Celery, RQ, or a cloud queue) once ingestion volume grows — `BackgroundTasks` runs in-process and doesn't survive a restart.
- **Observability**: log query, retrieved chunk IDs, similarity scores, and final answer for every request — this is what makes debugging bad answers possible later.

Next: [`05-production-best-practices.md`](05-production-best-practices.md) — chunking tuning, evaluation, caching, and security.
