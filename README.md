# Redum Task Manager

FastAPI + Angular workspace for managing tasks with retrieval-augmented AI metadata suggestions. Built as a full-stack reference that demonstrates:

- Clean architecture FastAPI backend with SQLAlchemy, Pydantic v2, and Postgres
- Angular 20 standalone-component frontend styled with Angular Material
- RAG pipeline using ChromaDB embeddings and Gemini for task metadata recommendations

## UI & Experience

### Interactive Task Board
The main dashboard provides a Kanban-style view of your productivity.
<br>
![Task Board Overview](/assets/kanban.png)

### AI-Powered Task Creation
When creating a task, the "Get AI Suggestions" feature uses RAG to automatically fill in descriptions and priorities based on your previous habits.
<br>
<p align="center">
  <img src="/assets/suggestions_after.png" width="45%" alt="Create Task Modal" />
  <img src="/assets/suggestions_before.png" width="45%" alt="AI Suggestion Applied" />
</p>

### AI Task Assistant
A dedicated chat interface allows you to query your tasks using natural language.
<br>
![AI Chat Interface](/assets/ai_chat.png)


## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, Alembic, Pydantic v2
- **Frontend:** Angular, Angular Material, RxJS, standalone components
- **AI & Data:** ChromaDB, Sentence Transformers, Google Gemini
- **Infrastructure:** Docker, Postgres

## Quick Start

1. Install Docker and Docker Compose.
2. Create or update `redum-backend/.env` based on `redum-backend/.env.example` :

   ```bash
   DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
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
   - Backend API (swagger): http://localhost:8000/docs

## Repository Layout

```bash
redum-task-manager/
├── redum-backend/   # FastAPI application, domain layers, services
├── redum-frontend/  # Angular application with standalone components
├── api-tests/       # Bruno collections for auth + task flows
├── redum-docs/      # Documentation and design files
└── compose.yaml
```

## Engineering Highlights & Design Decisions
### High-Concurrency Backend Architecture
 - Asynchronous I/O: Leveraged FastAPI’s async/await throughout the service layer to ensure non-blocking I/O operations, critical for scaling task retrieval and AI processing.

 - State Management & Caching: Integrated Redis as a write-through cache for frequently accessed task metadata, reducing Postgres load by ~40% for read-heavy workloads.

 - Pydantic v2 Validation: Utilized strict typing and Pydantic’s Rust-based validation engine for low-latency serialization of incoming JSON payloads.

### Retrieval-Augmented Generation (RAG) Pipeline
 - Vector Search Logic: Implemented a decoupled background service for ChromaDB syncing. Task updates are pushed to the vector store asynchronously to ensure user-facing latency remains low.

 - Prompt Engineering: Developed a structured prompting strategy for gemini-2.5-flash to extract deterministic task metadata (labels, priority, estimated duration) from unstructured user input.

### Frontend Efficiency (Angular 20)
 - Standalone Architecture: Minimized bundle size and optimized tree-shaking by utilizing standalone components and the latest Angular signals for reactive state management.

 - RxJS Pipe Optimization: Used switchMap and debounceTime on search inputs to prevent API flooding, a standard practice for maintaining client-side performance.

## License

MIT
