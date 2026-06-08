# ARCHITECTURE.md

# Stumi Research Architecture

Technical architecture documentation for Stumi Research v1.

---

# Overview

Stumi Research is a Retrieval-Augmented Generation (RAG) system designed for academic journal analysis.

The platform enables users to:

* Ingest academic papers from PDF URLs
* Extract metadata automatically
* Generate vector embeddings
* Perform semantic search
* Ask questions directly to a paper using AI

---

# High-Level Architecture

```text
                    ┌───────────────┐
                    │     User      │
                    └───────┬───────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ FastAPI Backend  │
                  └───────┬──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼

 ┌─────────────┐  ┌──────────────┐  ┌─────────────┐
 │ OpenRouter  │  │ PostgreSQL   │  │ PDF Source  │
 │    APIs     │  │ + pgvector   │  │ (Arxiv etc) │
 └─────────────┘  └──────────────┘  └─────────────┘
```

---

# System Components

## API Layer

Technology:

```text
FastAPI
```

Responsibilities:

* Receive HTTP requests
* Validate payloads
* Execute business logic
* Return JSON responses

Endpoints:

```text
GET    /health

POST   /journals/
GET    /journals/
GET    /journals/{id}

PATCH  /journals/{id}/hide
PATCH  /journals/{id}/unhide

DELETE /journals/{id}

POST   /journals/search

POST   /chat/
```

---

## Metadata Extraction

Purpose:

Extract journal metadata automatically.

Generated fields:

```text
Title
Authors
Institution
Publication Year
Abstract
```

Model:

```text
DeepSeek Chat
```

Provider:

```text
OpenRouter
```

---

## Embedding Service

Purpose:

Convert text into vector representations.

Model:

```text
BAAI BGE-M3
```

Provider:

```text
OpenRouter
```

Dimension:

```text
1024
```

Generated For:

```text
Abstract
Document Chunks
User Queries
```

---

## Chunking Engine

Purpose:

Split large documents into manageable semantic units.

Flow:

```text
PDF Text
    ↓
Clean Text
    ↓
Chunking
    ↓
Embeddings
```

Output:

```text
Chunk #1
Chunk #2
Chunk #3
...
Chunk #N
```

Stored in database.

---

# Database Architecture

Technology:

```text
PostgreSQL 18
```

Vector Extension:

```text
pgvector
```

---

## Journals Table

```text
journals
```

Stores:

* Metadata
* Abstract
* Abstract embedding
* PDF URL

Relationship:

```text
1 Journal
    ↓
Many Chunks
```

---

## Chunks Table

```text
chunks
```

Stores:

* Chunk text
* Vector embedding
* Chunk index

Purpose:

Retrieval during semantic search and RAG.

---

# Database Schema

```text
journals
│
├── id
├── title
├── normalized_title
├── authors
├── institution
├── publication_year
├── abstract
├── abstract_embedding
├── pdf_url
└── is_public

chunks
│
├── id
├── journal_id
├── chunk_text
├── embedding
└── chunk_index
```

Relationship:

```text
journals.id
        │
        ▼
chunks.journal_id
```

---

# Journal Ingestion Flow

```text
User
 │
 ▼
Submit PDF URL
 │
 ▼
Download PDF
 │
 ▼
Extract Text
 │
 ▼
Extract Metadata
 │
 ▼
Duplicate Check
 │
 ▼
Generate Abstract Embedding
 │
 ▼
Create Journal Record
 │
 ▼
Chunk Document
 │
 ▼
Generate Chunk Embeddings
 │
 ▼
Store Chunks
 │
 ▼
Done
```

---

# Semantic Search Flow

User query:

```text
machine translation with attention
```

Process:

```text
Query
 │
 ▼
Embedding
 │
 ▼
pgvector Similarity Search
 │
 ▼
Rank Results
 │
 ▼
Return Journals
```

SQL Similarity:

```sql
1 - (
  abstract_embedding <=> query_embedding
)
```

---

# RAG Flow

User question:

```text
What is Transformer?
```

Process:

```text
Question
 │
 ▼
Embedding
 │
 ▼
Retrieve Top Chunks
 │
 ▼
Build Context
 │
 ▼
LLM Prompt
 │
 ▼
Generate Answer
 │
 ▼
Return Answer + Sources
```

---

# Retrieval Pipeline

```text
Question
    ↓
Embedding

    ↓

Top-K Search

    ↓

Relevant Chunks

    ↓

Context Assembly

    ↓

DeepSeek Chat

    ↓

Answer
```

---

# Infrastructure Architecture

Production Environment:

```text
Ubuntu VPS
1 vCPU
1 GB RAM
60 GB SSD
```

---

## Web Layer

```text
Nginx
```

Responsibilities:

* HTTPS termination
* Reverse proxy
* SSL management

---

## Application Layer

```text
FastAPI
```

Managed by:

```text
systemd
```

---

## Data Layer

```text
PostgreSQL
```

Extensions:

```text
pgvector
```

---

# Production Request Flow

```text
Internet
    │
    ▼
Nginx
    │
    ▼
FastAPI
    │
    ▼
Service Layer
    │
    ▼
Database
```

For AI requests:

```text
FastAPI
    │
    ▼
OpenRouter
    │
    ├── Embeddings
    └── DeepSeek
```

---

# Security Architecture

Implemented:

```text
HTTPS
Rate Limiting
Swagger Disabled
OpenAPI Disabled
Systemd Isolation
```

Rate Limit:

```text
20 requests / minute
```

Protected Endpoint:

```text
/chat/
```

---

# Backup Architecture

Database backups:

```text
pg_dump
```

Schedule:

```text
Daily
02:00 AM
```

Retention:

```text
7 days
```

Storage:

```text
/home/stumi/backups
```

---

# Current Scalability

Current Server:

```text
1 vCPU
1 GB RAM
```

Expected Capacity:

### Journal Ingestion

```text
~5–20 journals/hour
```

depending on:

* PDF size
* OpenRouter latency

### Search

```text
Hundreds per day
```

### Chat

```text
Hundreds per day
```

before infrastructure becomes bottleneck.

---

# Cost Architecture

OpenRouter Models:

### Embedding

```text
BAAI BGE-M3

$0.01 / 1M tokens
```

### Chat

```text
DeepSeek Chat

Input:
$0.2002 / 1M tokens

Output:
$0.8001 / 1M tokens
```

Current expectation:

```text
Infrastructure cost
>
AI API cost
```

for small deployments.

---

# Future Architecture

## v2 Frontend

```text
Next.js
```

Features:

* Search UI
* Chat UI
* Journal browser

---

## Multi-Tenant Architecture

Future:

```text
Organization
    ├── Users
    ├── Roles
    ├── Permissions
    └── Documents
```

---

## Enterprise Knowledge Base

Target Markets:

* Internal Knowledge Base
* Customer Support AI
* Sales Enablement AI
* Compliance AI

---

# Architecture Principles

Stumi follows:

### Simplicity First

Single VPS deployment.

### Cost Efficiency

Low operational cost.

### AI-Native Design

Embedding-first architecture.

### Incremental Scaling

Scale only when usage requires it.

---

# Version

```text
Stumi Research v1
```

Status:

```text
Production Ready
```
