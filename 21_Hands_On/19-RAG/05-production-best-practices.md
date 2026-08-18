# 5. Production Best Practices

## 5.1 Evaluation — don't fly blind

Build a small evaluation set early: 20–50 realistic (question, expected answer / expected source) pairs pulled from real usage or written by someone who knows the domain.

Track at minimum:
- **Retrieval precision/recall** — did the top-K chunks actually contain the needed info?
- **Answer correctness** — is the generated answer factually right, judged against your expected answers?
- **Groundedness** — does every claim in the answer trace back to a retrieved chunk (i.e., no hallucination beyond the context)?
- **Citation accuracy** — do the cited sources actually support the claims next to them?

A simple approach: use an LLM-as-judge to score groundedness and correctness against your eval set, and re-run it whenever you change chunking, the embedding model, or the prompt. Treat this like a regression test suite for a normal codebase — RAG quality regresses silently otherwise.

## 5.2 Chunking tuning

- If answers are missing details that exist in the source doc → **decrease chunk size** or **increase overlap**.
- If answers pull in irrelevant/contradictory info → **decrease chunk size** or improve **structure-aware splitting** (don't split mid-table, mid-code-block, mid-list).
- If retrieval consistently returns the *wrong section entirely* → the problem is usually the embedding model or query phrasing, not chunk size — consider hybrid search or re-ranking (see 2.4).
- Always keep chunk metadata (source file, page number, section heading) — needed for citations and debugging.

## 5.3 Caching

Two layers worth caching:
- **Embedding cache**: never re-embed identical text. Hash the text (e.g. SHA-256) and store `hash → embedding` so re-ingestion or repeated queries skip the embedding API call.
- **Answer cache**: for frequently asked questions, cache `(question_hash, retrieved_chunk_ids) → answer` with a short TTL. Invalidate on document updates.

## 5.4 Keeping the index fresh

- **On document update**: delete all chunks for that `source` and re-ingest, rather than trying to diff/patch chunks — it's simpler and avoids stale partial chunks.
- **Versioning**: store a `document_version` or `updated_at` in metadata so you can filter out stale chunks if reprocessing is async and briefly overlaps.
- **Scheduled re-sync**: for data pulled from external systems (Confluence, Notion, a database), run a scheduled job that diffs source content and re-ingests only what changed.

## 5.5 Security & privacy

- **Tenant isolation**: always filter retrieval by tenant/user at the query level (see file 4.7) — never rely on the LLM to "only use the relevant parts" of mixed-tenant context.
- **PII handling**: if source documents contain PII, decide upfront whether it should be embedded at all, redacted before chunking, or access-controlled at retrieval time.
- **Prompt injection from retrieved content**: treat retrieved chunk content as untrusted — a malicious or compromised document could contain text like "ignore previous instructions." Keep the system prompt authoritative and consider a post-generation check if this is a real threat model for your data sources (e.g. user-uploaded documents from external parties).
- **Access control on citations**: if you show sources to the end user, make sure they're authorized to see that source document, not just that it matched.

## 5.6 Cost and latency

Typical latency budget for a query:
```
Embed query        ~50-150ms
Vector search       ~10-50ms
Re-rank (optional)  ~100-300ms
LLM generation      ~1-5s   (usually the bottleneck)
```

To reduce cost:
- Cache aggressively (5.3).
- Use a smaller/cheaper embedding model — embedding quality matters less than most people assume once you add re-ranking.
- Only re-rank when you retrieve a large candidate pool (e.g. top 20) — skip it for small corpora.
- Stream generation to the client so perceived latency drops even if total time doesn't.

## 5.7 Common failure modes

| Symptom | Likely cause |
|---|---|
| Answers confidently wrong | No "say I don't know" instruction, or retrieval returned irrelevant chunks that seemed plausible |
| Right document, wrong section | Chunk size too large; the needed fact is diluted by surrounding irrelevant text |
| Retrieval works, answer ignores context | Weak system prompt — be more explicit that the model must rely on context |
| Great in testing, bad in production | Eval set doesn't reflect real user queries — collect real queries and expand the eval set |
| Slow queries | No connection pooling, no ANN index on the vector column, or re-ranking a huge candidate pool |
| Cross-tenant data leakage | Filtering done in application code instead of the database query |

## 5.8 A pragmatic rollout checklist

- [ ] Chunking strategy chosen and documented (size, overlap, structure-aware or not)
- [ ] Embedding model + vector DB selected, ANN index created
- [ ] Ingestion pipeline handles re-ingestion (delete-then-insert) on document update
- [ ] Retrieval filtered by tenant/access control at the SQL/DB level
- [ ] System prompt enforces grounding + "I don't know" behavior
- [ ] Sources returned to the client alongside every answer
- [ ] Evaluation set (20+ Q&A pairs) with a repeatable scoring script
- [ ] Logging of query, retrieved chunk IDs, similarity scores, final answer
- [ ] Rate limiting on query and ingestion endpoints
- [ ] Caching for embeddings and (optionally) frequent answers

Next: [`06-architecture-diagrams.md`](06-architecture-diagrams.md) — visual summaries of the full system.
