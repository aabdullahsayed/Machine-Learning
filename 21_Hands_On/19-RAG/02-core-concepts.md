# 2. Core Concepts

## 2.1 Embeddings

An **embedding** is a numeric vector (e.g. 768 or 1536 floats) that represents the *meaning* of a piece of text. Texts with similar meaning end up close together in vector space, even if they use different words.

Example (conceptually):
```
embed("How do I reset my password?")      → [0.12, -0.44, 0.03, ...]
embed("Steps to change your login pass")  → [0.11, -0.42, 0.05, ...]   ← close to the above
embed("What's the weather today?")        → [0.88,  0.10, -0.71, ...] ← far from the above
```

Similarity is usually measured with **cosine similarity** or **dot product**.

Common embedding models:
- OpenAI `text-embedding-3-small` / `text-embedding-3-large`
- Voyage AI `voyage-3` (strong for retrieval, works well with Claude)
- Cohere `embed-v3`
- Open source: `bge-large`, `e5-large`, `nomic-embed-text` (run locally via sentence-transformers)

Things that matter when picking one:
- **Dimensionality** — higher isn't always better; affects storage and search speed.
- **Max input tokens** — how much text you can embed per chunk.
- **Domain fit** — general-purpose models work fine for most text; specialized domains (legal, medical, code) sometimes benefit from domain-tuned models.
- **Cost & latency** — you'll call this on every ingested chunk and every query.

## 2.2 Chunking

You can't embed an entire 200-page PDF as one vector — you'd lose specificity and hit token limits. So you split documents into **chunks** first.

### Common strategies

| Strategy | How it works | Best for |
|---|---|---|
| **Fixed-size** | Split every N tokens/characters, with overlap | Quick prototypes, homogenous text |
| **Recursive character splitting** | Try splitting on paragraphs, then sentences, then words, until chunks fit | General-purpose default |
| **Semantic chunking** | Split where meaning shifts (via embedding similarity between sentences) | Long-form, topic-shifting docs |
| **Structure-aware** | Split on markdown headers, HTML tags, code function boundaries | Docs, code, structured content |

### Key parameters
- **Chunk size**: typically 200–800 tokens. Smaller = more precise retrieval but less context per chunk. Larger = more context but noisier retrieval.
- **Overlap**: typically 10–20% of chunk size, so a fact split across a chunk boundary still appears in at least one full chunk.

### Rule of thumb
Start with recursive splitting, ~500 tokens, ~50 token overlap. Tune from there based on evaluation (see file 5).

## 2.3 Vector databases

A vector database stores embeddings alongside metadata and supports fast **approximate nearest neighbor (ANN)** search.

| Option | Type | Notes |
|---|---|---|
| **pgvector** | Postgres extension | Great if you already use Postgres; no new infra |
| **Chroma** | Embedded / local | Easiest for prototyping, single-process |
| **Qdrant** | Standalone service | Good filtering support, easy self-host or cloud |
| **Pinecone** | Managed cloud | Zero-ops, scales well, paid |
| **Weaviate** | Standalone service | Hybrid search built-in |
| **Milvus** | Standalone service | Built for very large scale |

For most backend applications, **pgvector** (if you already run Postgres) or **Qdrant** (if you want a dedicated vector service) are solid defaults.

## 2.4 Retrieval

At query time:
1. Embed the user's query with the *same* embedding model used for the documents.
2. Search the vector DB for the top-K most similar chunks (K is typically 3–10).
3. Optionally filter by metadata (e.g. `tenant_id`, `document_type`, `date_range`).

### Hybrid search
Pure vector search misses exact keyword matches (IDs, error codes, product SKUs). **Hybrid search** combines vector similarity with traditional keyword search (BM25) and merges the results. Most vector DBs support this natively now.

### Re-ranking
Initial retrieval (vector or hybrid) is optimized for speed, not precision. A common pattern:
1. Retrieve top 20–50 candidates cheaply (vector search).
2. Re-rank them with a more expensive, more accurate **cross-encoder re-ranker** (e.g. Cohere Rerank, `bge-reranker`).
3. Keep only the top 3–5 after re-ranking.

This two-stage approach ("retrieve then re-rank") consistently improves answer quality.

## 2.5 Context assembly & prompting

Once you have your top chunks, build a prompt like:

```
You are a helpful assistant. Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't know.

Context:
[1] (source: policy.pdf, page 4)
"Employees are entitled to 15 days of paid leave per year..."

[2] (source: policy.pdf, page 5)
"Unused leave carries over up to a maximum of 5 days..."

Question: How many leave days carry over?

Answer (cite sources like [1], [2]):
```

Key design choices:
- **Grounding instruction** — explicitly tell the model to only use the provided context, and to admit when it doesn't know.
- **Source tags** — include a source identifier per chunk so the model can cite it, and so you can verify/display provenance to the user.
- **Ordering** — put the most relevant chunk closest to the question (some models pay more attention to text near the end of the prompt).

## 2.6 Generation

The final step is a normal LLM call, just with the retrieved context injected. Nothing special here beyond standard prompting — but the quality of everything upstream (chunking, retrieval, re-ranking) determines whether the LLM has good material to work with. Garbage retrieval → garbage answer, regardless of model quality.

Next: [`03-building-the-pipeline.md`](03-building-the-pipeline.md) — putting these pieces together into a working pipeline.
