# AI Microservice Platform (RAG Chat System)

A full-stack Retrieval-Augmented Generation (RAG) platform built with React, FastAPI, PostgreSQL, Qdrant, and Ollama.

The platform allows users to upload documents, generate vector embeddings, perform semantic search, and receive AI-generated answers grounded in uploaded document content.

---

## Features

- Document Upload (.txt)
- PostgreSQL Metadata Storage
- Vector Embeddings with Sentence Transformers
- Qdrant Vector Database
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Local LLM Inference using Ollama
- Dockerized Microservice Architecture
- Chat History Persistence

---

## Architecture

```text
React Frontend
       ↓
FastAPI Backend
       ↓
PostgreSQL
       ↓
Qdrant Vector Database
       ↓
Sentence Transformers
       ↓
Ollama (Llama 3.2)
```

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript

### Backend

- FastAPI
- Python
- SQLAlchemy
- Pydantic

### Databases

- PostgreSQL
- Qdrant

### AI Components

- Sentence Transformers
- Ollama
- Llama 3.2
- Retrieval-Augmented Generation (RAG)

### Infrastructure

- Docker
- Docker Compose

---

## Project Structure

```text
rag-chat-platform/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── embedding_utils.py
│   ├── llm_utils.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

---

## How It Works

### Document Ingestion

1. User uploads a document.
2. Document metadata is stored in PostgreSQL.
3. Document is saved locally.

### Embedding Generation

1. Document text is split into chunks.
2. Sentence Transformers generate embeddings.
3. Embeddings are stored in Qdrant.

### Semantic Search

1. User submits a question.
2. Question is embedded.
3. Qdrant retrieves relevant document chunks.

### AI Response Generation

1. Retrieved chunks are injected into a prompt.
2. Ollama generates a grounded response.
3. Response is returned to the frontend.

---

## Example Query

Question:

```text
What stores application data?
```

Response:

```text
PostgreSQL stores application data.
```

---

## Running the Project

### Build Containers

```bash
docker compose up --build
```

### Frontend

```text
http://localhost:5173
```

### Backend

```text
http://localhost:8000
```

### FastAPI Docs

```text
http://localhost:8000/docs
```

### Qdrant Dashboard

```text
http://localhost:6333/dashboard
```

---

## Future Improvements

- PDF Upload Support
- OCR Support
- Streaming Responses
- User Authentication
- Multi-user Support
- Kubernetes Deployment
- AWS Deployment
- Hybrid Search
- Citation Generation
- Conversation Memory

---

## Author

Jeremiah Ulate

Texas Tech University  
M.S. Computer Science
