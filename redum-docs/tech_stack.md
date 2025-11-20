# Redum Task Manager Technical Stack Overview

## Architecture Summary
Redum Task Manager is a modern web application built on a **Clean Architecture** pattern. It features a decoupled **FastAPI** backend and an **Angular 20** frontend. The system leverages a **Retrieval-Augmented Generation (RAG)** engine for AI-powered task suggestions, utilizing a dual-vector store strategy with **ChromaDB** (local development) and **Pinecone** (production/cloud) via a unified protocol.

## Technology Stack & Implementation

| Technology | Category | Location in Code | Usage Description |
| :--- | :--- | :--- | :--- |
| **FastAPI** | Backend Framework | `redum-backend/app/main.py` | Core API framework handling request routing, validation, and dependency injection. |
| **Angular 20** | Frontend Framework | `redum-frontend/src/main.ts` | Single Page Application (SPA) framework using standalone components and Signals for state management. |
| **SQLAlchemy** | ORM | `redum-backend/app/infrastructure/database` | Database abstraction layer for PostgreSQL interactions using the Session pattern. |
| **PostgreSQL** | Database | `docker-compose.yml` | Primary relational database for storing users, tasks, and application state. |
| **Pydantic** | Data Validation | `redum-backend/app/domain/schemas` | Defines data schemas for API request/response validation and settings management. |
| **Alembic** | Database Migration | `redum-backend/alembic` | Handles database schema migrations and version control. |
| **ChromaDB** | Vector Store | `redum-backend/app/infrastructure/vector_stores/chroma.py` | Local vector store implementation for storing task embeddings during development. |
| **Pinecone** | Vector Store | `redum-backend/app/infrastructure/vector_stores/pinecone.py` | Serverless cloud vector store implementation for production-grade similarity search. |
| **Google Gemini** | LLM | `redum-backend/app/services/ai_service.py` | Generative AI model used for generating task metadata suggestions based on context. |
| **Sentence Transformers** | Embeddings | `redum-backend/app/infrastructure/vector_stores` | Generates vector embeddings (`all-MiniLM-L6-v2`) for task text to enable semantic search. |
| **Angular Material** | UI Component Library | `redum-frontend/src/app` | Provides pre-built, accessible UI components (Cards, Dialogs, Sidenav) following Material Design 3. |
| **RxJS** | Reactive Programming | `redum-frontend/src/app/core/services` | Handles asynchronous data streams and HTTP requests in the frontend. |

## Component Deep Dive

### 1. Backend Architecture (Clean Architecture)
The backend is structured to separate concerns into distinct layers, ensuring maintainability and testability.

*   **API Layer** (`app/api/v1`): Contains route handlers that parse requests and call services. It relies on Pydantic schemas for validation.
*   **Service/Use Case Layer** (`app/services`, `app/use_cases`): Implements business logic. It orchestrates data flow between the API and the Repository layers.
*   **Domain Layer** (`app/domain`): Defines the core business entities (SQLAlchemy models) and data transfer objects (Pydantic schemas).
*   **Infrastructure Layer** (`app/infrastructure`): Handles external concerns like database connections (`repositories`) and vector store implementations.

### 2. RAG System & Vector Store Abstraction
The AI features are built on a flexible RAG architecture designed to support multiple vector database backends.

*   **Protocol Definition**: `VectorStoreProtocol` (`app/core/vector_store.py`) defines the contract (`add_documents`, `query`, `delete`) that all vector stores must adhere to.
*   **Implementations**:
    *   **ChromaVectorStore**: Wraps `chromadb` for a local, file-based vector store. It uses a custom `_EmbeddingFunctionWrapper` to adapt `sentence-transformers`.
    *   **PineconeVectorStore**: Wraps the `pinecone-client` for cloud-based storage. It handles index creation (using Serverless AWS specs) and batch upserting.
*   **AI Service**: `RAGService` (`app/services/ai_service.py`) injects the configured `VectorStoreProtocol`. It manages the flow of embedding task data, querying for similar tasks, and prompting Google Gemini to suggest metadata.

### 3. Frontend Architecture (Angular Standalone)
The frontend adopts the modern Angular "Standalone" architecture, removing the need for `NgModule`.

*   **State Management**: Uses Angular **Signals** for granular reactivity. Services (e.g., `TaskService`) expose state as read-only signals, which components consume to update the UI efficiently.
*   **Zoneless Change Detection**: Configured in `app.config.ts` (`provideZonelessChangeDetection()`) for improved performance.
*   **Lazy Loading**: Routes are defined in `app.routes.ts` using `loadComponent`, ensuring that feature modules (Auth, Tasks) are loaded only when needed.
