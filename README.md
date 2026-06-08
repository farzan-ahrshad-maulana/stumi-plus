# Stumi Research

AI-powered research assistant for academic papers using Retrieval-Augmented Generation (RAG).

Stumi allows users to ingest research papers, perform semantic search across journals, and ask questions directly to a paper using AI.

---

## Features

### Journal Ingestion

* Download PDF from URL
* Extract metadata automatically
* Extract abstract
* Detect duplicate journals
* Chunk document into semantic passages
* Generate embeddings
* Store vectors in PostgreSQL + pgvector

### Semantic Search

Search journals using natural language.

Example:

```text
machine translation with attention
```

Returns the most relevant papers based on vector similarity.

### RAG Chat

Ask questions directly to a journal.

Example:

```text
What is Transformer?
```

Stumi retrieves the most relevant chunks and generates an answer using an LLM.

### Journal Management

* List journals
* View journal details
* Hide journal
* Unhide journal
* Delete journal

### Production Features

* HTTPS
* Nginx Reverse Proxy
* PostgreSQL
* pgvector
* Rate Limiting
* Automated Backup
* Systemd Service

---

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* pgvector

### AI

* BAAI BGE-M3 Embeddings
* DeepSeek Chat
* OpenRouter

### Infrastructure

* Ubuntu VPS
* Nginx
* Systemd

---

## Architecture

```text
PDF URL
   ↓
PDF Download
   ↓
Metadata Extraction
   ↓
Chunking
   ↓
Embedding Generation
   ↓
PostgreSQL + pgvector
   ↓
Semantic Retrieval
   ↓
LLM
   ↓
Answer
```

---

## API Endpoints

### Health Check

```http
GET /health
```

### Ingest Journal

```http
POST /journals/
```

Request:

```json
{
  "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf"
}
```

### Search Journals

```http
POST /journals/search
```

Request:

```json
{
  "query": "machine translation",
  "limit": 10
}
```

### Chat with Journal

```http
POST /chat/
```

Request:

```json
{
  "journal_id": 1,
  "question": "What is Transformer?"
}
```

---

## Local Development

Clone repository:

```bash
git clone <repository-url>

cd stumi
```

Create virtual environment:

```bash
python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost/stumi

OPENROUTER_API_KEY=your_key
```

Run application:

```bash
uvicorn app.main:app --reload
```

---

## Production

Production deployment guide:

```text
DEPLOYMENT.md
```

Production operations guide:

```text
OPERATIONS.md
```

System architecture:

```text
ARCHITECTURE.md
```

---

## Project Status

Current Version:

```text
Stumi Research v1
```

Implemented:

* Journal ingestion
* Semantic search
* RAG chat
* Rate limiting
* Backup automation
* Production deployment

Planned:

* Frontend UI
* User authentication
* Multi-tenant workspaces
* Enterprise knowledge base
* Role-based access control

---

## License

MIT License
