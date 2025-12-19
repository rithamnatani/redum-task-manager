# Redum Task Manager

FastAPI + Angular workspace for managing tasks with retrieval-augmented AI metadata suggestions. Built as a full-stack reference that demonstrates:

- Clean architecture FastAPI backend with SQLAlchemy, Pydantic v2, Postgres, and Redis caching
- Angular 20 standalone-component frontend styled with Angular Material
- RAG pipeline using ChromaDB embeddings and Google Gemini (`gemini-2.5-flash`) for task metadata recommendations

## Tech Stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy, Alembic, Pydantic v2
- **Frontend:** Angular 20, Angular Material, RxJS, standalone components
- **AI & Data:** ChromaDB, Sentence Transformers, Google Gemini Generative AI
- **Infrastructure:** Docker Compose, Postgres 15, Redis 7, Bruno API collections

## Quick Start

1. Install Docker and Docker Compose.
2. Create or update `redum-backend/.env`:

   ```env
   DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
   REDIS_URL=redis://redis:6379/0
   SECRET_KEY=change-me
   GEMINI_API_KEY=your_gemini_key
   GEMINI_MODEL=gemini-2.5-flash
   CHROMA_DB_PATH=./chroma-storage
   ```

3. Launch the stack:

   ```bash
   docker compose up --build
   ```

4. Open the apps:
   - Frontend UI: http://localhost:8080
   - Backend API docs: http://localhost:8000/docs

### Helpful Commands

- Rebuild backend only: `docker compose build backend`
- Tail backend logs: `docker compose logs -f backend`

## Repository Layout

```
redum-task-manager/
├── redum-backend/   # FastAPI application, domain layers, services
├── redum-frontend/  # Angular application with standalone components
├── api-tests/       # Bruno collections for auth + task flows
├── redum-infra/     # Infrastructure stubs and IaC placeholders
├── redum-docs/      # Documentation and design files
└── docker-compose.yml
```

## Highlight Features

- JWT-based auth with role-ready architecture
- Task CRUD synced to ChromaDB for relevance-aware AI suggestions
- Gemini-backed `/api/v1/tasks/suggest` endpoint, surfaced in the Angular create-task dialog
- Docker-first workflow for reproducible local environments

## License

MIT 

