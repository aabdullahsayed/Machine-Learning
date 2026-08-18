# 6. Architecture Diagrams

## 6.1 Full system overview

```
┌────────────────────────────────────────────────────────────────────┐
│                          INGESTION (offline)                        │
│                                                                       │
│  Documents ──► Extract text ──► Chunk ──► Embed ──► Store in Vector  │
│  (PDF/HTML/                                             DB           │
│   DOCX/DB rows)                                    (with metadata:   │
│                                                     source, tenant,   │
│                                                     page, etc.)       │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                            QUERY (online)                            │
│                                                                       │
│   Client                                                              │
│     │  POST /query {question, tenant_id}                             │
│     ▼                                                                 │
│   Backend API (FastAPI/Express/etc.)                                  │
│     │                                                                 │
│     ├─► Embed question ────────────────┐                              │
│     │                                   ▼                              │
│     ├─► Vector search (filtered   ┌───────────┐                        │
│     │    by tenant_id)  ◄─────────┤ Vector DB │                        │
│     │                             └───────────┘                        │
│     │        (optional: re-rank top candidates)                        │
│     │                                                                 │
│     ├─► Assemble prompt (question + retrieved chunks + citations)     │
│     │                                                                 │
│     ├─► Call LLM ─────────────────► ┌─────┐                           │
│     │                                │ LLM │                           │
│     │        ◄───────────────────── └─────┘                           │
│     │                                                                 │
│     ▼                                                                 │
│   Response { answer, sources[] }                                      │
│     │                                                                 │
│     ▼                                                                 │
│   Client renders answer + citations                                   │
└────────────────────────────────────────────────────────────────────┘
```

## 6.2 Ingestion pipeline detail

```
 upload.pdf
     │
     ▼
┌─────────────┐
│ Extract text │  (pypdf / html parser / docx parser)
└──────┬───────┘
       ▼
┌─────────────┐
│   Chunk      │  recursive split, ~500 tokens, ~50 overlap
└──────┬───────┘
       ▼
┌─────────────┐
│   Embed      │  batch call to embedding API
└──────┬───────┘
       ▼
┌─────────────┐
│ Store rows   │  (source, chunk_index, content, embedding, metadata)
└─────────────┘
```

## 6.3 Retrieval + re-ranking detail

```
query ──► embed query
             │
             ▼
      vector search (top 20-50)
             │
             ▼
   ┌───────────────────┐
   │  cross-encoder     │   optional but recommended
   │  re-ranker          │   at moderate-to-large scale
   └─────────┬───────────┘
             ▼
       top 3-5 chunks
             │
             ▼
      prompt assembly
             │
             ▼
          LLM call
```

## 6.4 Multi-tenant data isolation

```
                     ┌────────────────────────────┐
                     │        documents table       │
                     ├───────────┬──────────────────┤
                     │ tenant_id │ content, embedding│
                     ├───────────┼──────────────────┤
Tenant A query ──────►  = 'A'    │ ...only A's rows  │
                     ├───────────┼──────────────────┤
Tenant B query ──────►  = 'B'    │ ...only B's rows  │
                     └───────────┴──────────────────┘

Filter applied in the SQL WHERE clause — never in application logic after
the fact, and never trust the LLM to "ignore" other tenants' context.
```

---

This completes the guide. See `README.md` for the full index, and `04-backend-integration.md` for copy-pasteable, runnable code.
