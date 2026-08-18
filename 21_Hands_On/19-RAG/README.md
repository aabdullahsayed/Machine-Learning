# RAG (Retrieval-Augmented Generation) — Complete Guide

A practical, from-scratch guide to understanding RAG and integrating it into a real backend application.

## Contents

1. [`01-what-is-rag.md`](01-what-is-rag.md) — What RAG is, why it exists, when to use it
2. [`02-core-concepts.md`](02-core-concepts.md) — Embeddings, vector stores, chunking, retrieval, re-ranking
3. [`03-building-the-pipeline.md`](03-building-the-pipeline.md) — Step-by-step: ingest → chunk → embed → store → retrieve → generate
4. [`04-backend-integration.md`](04-backend-integration.md) — Wiring RAG into a FastAPI backend (full working code)
5. [`05-production-best-practices.md`](05-production-best-practices.md) — Chunking strategy, evaluation, caching, security, scaling
6. [`06-architecture-diagrams.md`](06-architecture-diagrams.md) — Text-based diagrams of the full system

## Suggested reading order

If you're new to RAG: read files 1 → 5 in order.
If you already understand the concept and just want to wire it into an app: jump straight to `04-backend-integration.md`, and use `02` and `05` as reference.

## What you'll be able to build after this

A backend service where a client sends a question, the service retrieves relevant chunks from your own documents (PDFs, docs, database rows, etc.), and returns an LLM-generated answer grounded in that retrieved context — with citations back to source documents.
