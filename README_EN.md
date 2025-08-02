# MiniRAG

<p align="center">
    <a href=""><img src="https://img.shields.io/badge/MiniRAG-brightgreen.svg"></a>
    <img src="https://img.shields.io/badge/LangChain-blue">
    <img src="https://img.shields.io/badge/LangGraph-blue">
    <img src="https://img.shields.io/badge/PGVector-blue">
</p>

A minimal RAG (Retrieval-Augmented Generation) system for knowledge-based question answering, using PGVector for document storage and retrieval, combined with SiliconFlow API for embedding and re-ranking.

## Features
Small but complete.
- Document reading and chunking
- Document embedding and vector storage
- Vector retrieval and re-ranking
- Retrieval optimization
- Workflow orchestration

## Dependencies

- Python 3.11+
- Main libraries:
  - `langchain`
  - `langgraph`

## Configuration

1. Copy `.env.example` to `.env` and fill in the following:
   ```
   SILICONFLOW_API_KEY=your_api_key
   PG_USER=your_db_user
   PG_PASSWORD=your_db_password
   PG_HOST=your_db_host
   PG_PORT=your_db_port
   ```
2. Ensure PostgreSQL database is running and properly configured.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run example scripts:
   ```bash
   python demo_embedding.py  # Document embedding example
   python demo_minirag.py    # QA system example
   ```

## Project Structure

```
├── .env                    # Environment variables
├── README.md               # Project description
├── demo_embedding.py       # Document embedding example
├── demo_minirag.py         # QA system example
├── src/
│   ├── config.py           # Configuration loader
│   ├── embedding.py        # Embedding logic
│   ├── prompts.py          # Prompt templates
│   ├── reranker.py         # Re-ranking logic
│   └── workflow.py         # Workflow definition
```

## PGVector Deployment
- Recommended to use Docker:
```
docker volume create pgvector
docker run -d \
  --name pgvector \
  -e POSTGRES_USER=username \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=database \
  -p 5432:5432 \
  -v pgvector:/var/lib/postgresql/data \
  ankane/pgvector
```