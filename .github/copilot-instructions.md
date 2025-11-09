# AI Agent Instructions for Redum Task Manager

## 1\. Project Overview

This is a full-stack, AI-augmented task management platform. It serves as a showcase of senior-level engineering skills, integrating modern practices in full-stack development (FastAPI/Angular), scalable cloud architecture (AWS ECS), and advanced RAG pipelines .

**Critical Architectural Note:** This is **NOT** a microservices architecture. The project consists of two main applications:

1.  **`redum-backend/`**: A **production-grade monolith** built with FastAPI, containing all business logic, API endpoints, and AI RAG services .
2.  **`redum-frontend/`**: A **standalone Single Page Application (SPA)** built with Angular .

## 2\. Core Architecture & Design Philosophy (Backend)

All code generated for the `redum-backend/` **MUST** adhere to these principles:

1.  **Clean Architecture:** The \#1 rule. Dependencies flow *inwards*. The framework (FastAPI) and database (SQLAlchemy) are "details" that depend on core business logic, not the other way around.
2.  **Thin Controllers (Routes):** FastAPI routes (in `/app/api/v1/endpoints/`) MUST be thin. Their *only* job is to parse requests, call a single Use Case/Service, and return a response. **No business logic in routes.**
3.  **Repository Pattern:** All database operations MUST be abstracted. Use Cases (e.g., `TaskService`) will depend on an *interface* (e.g., `ITaskRepository`) . The *implementation* (e.g., `SQLTaskRepository`) lives in the Infrastructure layer .
4.  **Service Layer (Use Cases):** All business logic (task creation, RAG orchestration) lives in the `/app/use_cases/` directory.
5.  **Dependency Injection (DI):** ALWAYS use FastAPI's `Depends` system to provide dependencies (DB sessions, services, repositories) to routes and other services. This is non-negotiable for testability .
6.  **Separate Models & Schemas:**
      * **`domain/models/`**: SQLAlchemy models (the database table structure) .
      * **`domain/schemas/`**: Pydantic models (the API data contracts for request/response) .

## 3\. Backend (FastAPI) File Structure

This is the non-negotiable file structure. All new code **MUST** be placed in the correct layer.

```
/backend/
│
├── app/
│   │
│   ├── api/                # 1. PRESENTATION LAYER (FastAPI Routes)
│   │   └── v1/
│   │       ├── endpoints/  # Thin routers (tasks.py, auth.py)
│   │       └── api.py
│   │
│   ├── use_cases/          # 2. APPLICATION LAYER (Business Logic)
│   │   ├── auth/           # (auth_service.py)
│   │   ├── tasks/          # (task_service.py)
│   │   └── ai/             # (rag_service.py, chat_service.py)
│   │
│   ├── domain/             # 3. DOMAIN LAYER (Core Rules & Data)
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── schemas/        # Pydantic DTOs (API Schemas)
│   │   └── interfaces/     # Abstract interfaces (e.g., vector_store_interface.py)
│   │
│   ├── infrastructure/     # 4. INFRASTRUCTURE LAYER (External Details)
│   │   ├── database/       # DB session management (session.py)
│   │   ├── repositories/   # Concrete repository implementations (task_repo.py)
│   │   ├── services/       # External API clients (pinecone_client.py, gemini_client.py)
│   │   └── cache/          # Redis client setup
│   │
│   ├── core/               # App-wide config, settings (config.py)
│   └── main.py             # App entrypoint, middleware, DI wiring
│
├── alembic/                # Alembic migration scripts
├── tests/                  # Pytest unit and integration tests
├── backend.Dockerfile      # Multi-stage production Dockerfile
└── docker-compose.yml      # Local dev environment
```

## 4\. Frontend (Angular) Architecture

1.  **Modularity:** The application **MUST** use the `CoreModule`, `SharedModule`, and `FeatureModule` pattern .
      * **`CoreModule`:** For singleton services (`AuthService`, `TaskService`), guards (`AuthGuard`), and interceptors (`JwtInterceptor`) . Import *only* in `AppModule`.
      * **`SharedModule`:** For re-usable components (e.g., spinners, modals) and pipes.
      * **`FeatureModules`:** For `Auth`, `Tasks`, and `Chat`.
2.  **State Management:** **DO NOT USE NgRx.** State will be managed using RxJS `BehaviorSubject`s within the singleton services provided in `CoreModule`.
3.  **Forms:** **MUST** use **Angular Reactive Forms** for all user input .

## 5\. Key Technology Stack

  * **Backend:** FastAPI, Pydantic, SQLAlchemy, Alembic
  * **Frontend:** Angular, TypeScript, Reactive Forms
  * **AI:** LangChain (LCEL), `sentence-transformers`, Gemini API, Pinecone
  * **Database/Cache:** PostgreSQL (AWS RDS), Redis (AWS ElastiCache)
  * **Infra/DevOps:** Docker, AWS ECS + Fargate, GitHub Actions

## 6\. Local Development Workflow

  * The backend, database, and cache are orchestrated by `docker-compose.yml` .
  * To run the full local backend stack: `docker-compose up --build`.
  * The frontend is run separately: `cd redum-frontend` and `ng serve`.

## 7\. Integration Points

  * **`redum-frontend`** calls **`redum-backend`** via REST API.
  ````instructions
  # AI Agent Instructions for Redum Task Manager

  This file documents factual, discoverable patterns that an AI coding agent must
  follow to be productive in `redum-backend/`. Keep routes thin, use the
  repository pattern, and place business logic in `app/use_cases/`.

  ## Core Architecture & non-negotiables
  - `redum-backend/` is a FastAPI monolith. Do NOT treat it as microservices.
  - Follow Clean Architecture: domain → use_cases → infrastructure → api.
  - Routes in `app/api/v1/endpoints/` must be thin: parse → call one use case → return.
  - Database access must go through repository interfaces in `app/domain/interfaces/`.

  ## File layout (must use)
  ```
  app/
    api/v1/endpoints/    # thin FastAPI routers (auth.py, tasks.py)
    use_cases/           # business logic (auth, tasks, ai)
    domain/
      models/            # SQLAlchemy models (DB tables)
      schemas/           # Pydantic request/response DTOs
      interfaces/        # abstract repository/service interfaces
    infrastructure/
      database/          # SQLAlchemy base/session wiring
      repositories/      # concrete repo implementations
      services/          # external clients (pinecone, llm)
      cache/             # Redis client setup
    core/                 # config, settings
    main.py               # FastAPI app factory and DI wiring

  alembic/                # alembic env + versions
  docker-compose.yml
  backend.Dockerfile
  tests/
  ```

  ## Concrete implementation checklist (do these in order)
  1. `app/core/config.py` — implement `Settings` (read DATABASE_URL, REDIS_URL, SECRET_KEY via env).
  2. `app/infrastructure/database/base.py` — expose `Base = declarative_base()`.
  3. `app/domain/models/user.py` and `task.py` — SQLAlchemy ORM models (User, Task).
     - Task fields: title, description, due_date, priority, user_id FK.
  4. `app/domain/schemas/*` — Pydantic: `UserCreate`, `TaskCreate`, `TaskRead`, `Token`.
     - Use `Config.orm_mode = True` on read schemas.
  5. `app/domain/interfaces/itask_repository.py` — define `ITaskRepository` (create, get_by_id, get_all_by_user, update, delete).
  6. `app/infrastructure/repositories/task_repository.py` — SQLAlchemy implementation of `ITaskRepository` (session-scoped).
  7. `app/use_cases/auth/` and `app/use_cases/tasks/` — `AuthService` and `TaskService` that depend on repositories.
  8. `app/api/v1/endpoints/auth.py` and `tasks.py` — very thin routers that `Depends()` services.
  9. `alembic/` — add `env.py` that reads DB URL from `app.core.config.Settings` and sets `target_metadata` from `infrastructure.database.base.Base.metadata`.
  10. Create initial migration and run `alembic upgrade head`.

  ## Alembic & migrations
  - Alembic should read DB URL from `app.core.config.Settings().DATABASE_URL`.
  - In `alembic/env.py` import settings (do not hardcode connection strings).
  - Autogenerate the first migration after step 3 is implemented.

  ## Containerization
  - `backend.Dockerfile` should be a multi-stage Python build (install deps, copy source, run uvicorn).
  - `docker-compose.yml` must provide services: `backend`, `postgres` (Postgres >= 13), `redis`.
    - Set environment variables for DB connectivity and create a simple health check for the backend.

  ## Examples & patterns (copyable)
  - Endpoint pattern (thin):

  ```py
  @router.post("/tasks", response_model=TaskRead)
  def create_task(payload: TaskCreate, svc: TaskService = Depends()):
      return svc.create_task(payload)
  ```

  - Repository contract example (interface):

  ```py
  class ITaskRepository(ABC):
      def create(self, *, task_create: TaskCreate) -> Task: ...
      def get_by_id(self, task_id: int) -> Optional[Task]: ...
  ```

  ## What to avoid
  - No business logic in routers.
  - Do not import SQLAlchemy sessions in `use_cases/` or `api/` — only in `infrastructure/repositories/` or `infrastructure/database`.

  ## Where to look
  - `app/api/v1/endpoints/` — router examples.
  - `app/use_cases/` — place business logic here.
  - `app/infrastructure/repositories/` — DB adapters live here.

  ---
  If you'd like, I can now scaffold the first implementation (models, schemas, interfaces, repository, one use-case and one thin endpoint) and add an `alembic/env.py` template. Tell me whether to proceed with implementation or only update this document further.
  ````