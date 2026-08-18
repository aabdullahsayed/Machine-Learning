# 1. What is RAG?

## The problem it solves

LLMs are trained on a fixed snapshot of data. This creates three problems:

- **Staleness** — the model doesn't know about anything that happened after its training cutoff, or anything private to your organization (internal docs, tickets, contracts, product data).
- **Hallucination** — when the model doesn't know something, it often generates a plausible-sounding but wrong answer instead of saying "I don't know."
- **No source of truth** — even when the model is right, you can't easily point to *where* the answer came from.

**Retrieval-Augmented Generation (RAG)** fixes this by giving the model relevant, up-to-date information *at query time*, instead of relying only on what it memorized during training.

## The core idea in one sentence

> Before asking the LLM to answer a question, first retrieve the most relevant pieces of your own data and stuff them into the prompt as context.

That's it. Everything else in this guide is about doing that well, efficiently, and at scale.

## RAG vs. fine-tuning vs. long context

| Approach | Good for | Bad for |
|---|---|---|
| **RAG** | Frequently changing data, large corpora, needing citations, cheap to update | Requires infra (vector store, pipeline), retrieval can miss relevant info |
| **Fine-tuning** | Teaching a model a *style*, *format*, or *behavior* | Expensive to update, doesn't reliably inject new *facts*, can't cite sources |
| **Long context (stuffing everything in the prompt)** | Small, static datasets | Expensive per-request, slow, doesn't scale past context window, "lost in the middle" problem |

In practice, production systems often combine RAG with a well-designed system prompt, and occasionally light fine-tuning for tone/format.

## The RAG lifecycle, at a glance

There are two distinct phases:

### Phase A — Indexing (offline, done ahead of time)
```
Raw documents → Split into chunks → Embed chunks → Store in a vector database
```

### Phase B — Query (online, happens per user request)
```
User question → Embed question → Search vector DB for similar chunks
              → Build a prompt with those chunks as context
              → Send to LLM → Return grounded answer (+ sources)
```

## A minimal mental model

```
                     ┌─────────────────┐
                     │   Your Documents │
                     └────────┬─────────┘
                              │ (offline, once / on update)
                        chunk + embed
                              │
                              ▼
                     ┌─────────────────┐
                     │  Vector Database │
                     └────────┬─────────┘
                              │ similarity search
User question ───embed───────┤
                              ▼
                     ┌─────────────────┐
                     │ Top-K relevant   │
                     │ chunks (context) │
                     └────────┬─────────┘
                              │
                    Prompt = question + context
                              │
                              ▼
                     ┌─────────────────┐
                     │       LLM        │
                     └────────┬─────────┘
                              │
                              ▼
                     Answer (grounded, with sources)
```

## When you actually need RAG

Use RAG when:
- You have a knowledge base that changes (docs, tickets, product catalog, policies, code).
- You need answers grounded in *your* data, not general internet knowledge.
- You need to cite sources / show provenance.
- Your data is too large to fit in a single prompt.

You probably **don't** need RAG when:
- Your data fits comfortably in the context window and doesn't change often (just pass it directly in the prompt).
- The task is pure generation/creativity with no factual grounding requirement.
- You need the model to perform an *action*, not answer a *question* (that's tool use / function calling, possibly combined with RAG).

Next: [`02-core-concepts.md`](02-core-concepts.md) — the building blocks: embeddings, chunking, vector stores, and retrieval.
