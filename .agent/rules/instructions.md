---
trigger: always_on
---

## 1. Overview
These instructions ensure AI coding assistants extend the Redum Task Manager without breaking established architecture or style. Every guideline is based on the actual backend (FastAPI + SQLAlchemy) and frontend (Angular 20 + Angular Material) implementations in this repository—no external best practices unless already reflected in the codebase.

## 2. File Category Reference
### Backend
- **backend-environment-files**
  - Examples: `redum-backend/.env`, `redum-backend/.python-version`
  - Conventions: Define connection strings (Postgres, Redis) and secrets for dev docker-compose; pin Python to 3.11.9 and read all config via `Settings`.
- **backend-deployment-config**
  - Examples: `redum-backend/backend.Dockerfile`, `redum-backend/docker-compose.yml`
  - Conventions: Build from `python:3.11-slim`, install `requirements.txt`, run `uvicorn`; compose file mounts code, loads `.env`, links Postgres/Redis.
- **backend-dependency-management**
  - Examples: `redum-backend/requirements.txt`
  - Conventions: Pin libraries compatible with FastAPI 0.95+/SQLAlchemy 1.4+/Pydantic v1; include extras (`uvicorn[standard]`, `passlib[bcrypt]`).
- **backend-migration-scripts**
  - Examples: `redum-backend/alembic/env.py`, `redum-backend/alembic/versions/001_add_task_status.py`
  - Conventions: Use Alembic with project `Settings` wiring, create enums via raw SQL prior to attaching columns, drop columns before enum types on downgrade.
- **backend-application-entrypoint**
  - Example: `redum-backend/app/main.py`
  - Conventions: Provide `create_app()` factory, register CORS, include routers under `/api/v1`, and run `Base.metadata.create_all` only for local startup.
- **backend-api-routing**
  - Examples: `redum-backend/app/api/v1/endpoints/auth.py`, `.../tasks.py`
  - Conventions: Declare module-level `APIRouter`, build services with `Depends(get_db)`, keep handlers thin, map service errors to `HTTPException`, set `response_model`.
- **backend-configuration**
  - Example: `redum-backend/app/core/config.py`
  - Conventions: `Settings` extends `BaseSettings`, normalizes CORS origins via validator, exposes `get_settings()` for DI.
- **backend-domain-interfaces**
  - Example: `redum-backend/app/domain/interfaces/itask_repository.py`
  - Conventions: Define abstract CRUD signatures returning domain models, use keyword-only parameters mirroring service expectations.
- **backend-domain-models**
  - Examples: `redum-backend/app/domain/models/task.py`, `.../user.py`
  - Conventions: Inherit from shared `Base`, declare enums (`TaskStatus`) with string values, keep persistence-focused (no business logic).
- **backend-domain-schemas**
  - Examples: `redum-backend/app/domain/schemas/task.py`, `.../user.py`
  - Conventions: Separate create/update/read models; use validators to convert enums to strings; avoid exposing sensitive fields in read models.
- **backend-database-layer**
  - Examples: `redum-backend/app/infrastructure/database/session.py`, `.../base.py`
  - Conventions: Create engine with `pool_pre_ping`, expose `SessionLocal`, offer `get_db()` generator for scoped sessions.
- **backend-repository-implementations**
  - Examples: `redum-backend/app/infrastructure/repositories/task_repository.py`, `.../user_repository.py`
  - Conventions: Accept `Session` via constructor, wrap CRUD with `add/commit/refresh`, return `None` on misses, support partial updates via `setattr` loop.
- **backend-use-cases**
  - Examples: `redum-backend/app/use_cases/tasks/task_service.py`, `.../auth/auth_service.py`
  - Conventions: Inject interfaces, convert results to Pydantic models (`model_validate`), enforce business rules (ownership, unique email), raise `HTTPException`/`ValueError` as needed.
- **backend-package-initializers**
  - Examples: `redum-backend/app/api/v1/endpoints/__init__.py`, `.../use_cases/tasks/__init__.py`
  - Conventions: Keep empty to mark packages; avoid side effects or implicit exports.

### Frontend
- **frontend-project-config**
  - Examples: `redum-frontend/angular.json`, `package.json`
  - Conventions: Use standalone component build (`@angular/build:application`), styles in SCSS, assets pulled from `public/`.
- **frontend-vscode-config**
  - Examples: `redum-frontend/.vscode/launch.json`, `.../tasks.json`
  - Conventions: Launch Chrome via npm scripts, reuse TypeScript problem matcher waiting for "bundle generation complete", recommend only `angular.ng-template`.
- **frontend-public-assets**
  - Examples: `redum-frontend/public/favicon.ico`, `src/index.html`
  - Conventions: Store static assets in `public/`; link fonts/icons via CDN in `index.html`.
- **frontend-entrypoint**
  - Examples: `redum-frontend/src/main.ts`, `.../app.ts`
  - Conventions: Bootstrap with `bootstrapApplication(App, appConfig)`; keep root component minimal, log bootstrap errors.
- **frontend-global-styles**
  - Examples: `redum-frontend/src/styles.scss`, `.../app.scss`
  - Conventions: Apply Material 3 theme via `mat.theme`, enforce light color scheme, reset `html/body` height and fonts.
- **frontend-app-shell**
  - Example: `redum-frontend/src/app/app.ts`
  - Conventions: Standalone component importing only `RouterOutlet`, expose signals, no feature logic.
- **frontend-app-configuration**
  - Examples: `redum-frontend/src/app/app.config.ts`, `app.routes.ts`
  - Conventions: Provide zoneless change detection, router, HttpClient with interceptors, async animations; configure routes via lazy `loadComponent` and guards.
- **frontend-guards**
  - Example: `redum-frontend/src/app/core/guards/auth.guard.ts`
  - Conventions: Functional guard injecting token storage + router, redirect unauthenticated users while preserving `returnUrl`.
- **frontend-interceptors**
  - Example: `redum-frontend/src/app/core/interceptors/token.interceptor.ts`
  - Conventions: Functional `HttpInterceptorFn` adding bearer token only for `/api/v1/` requests; append interceptors in `withInterceptors` array.
- **frontend-services**
  - Examples: `redum-frontend/src/app/core/services/task.service.ts`, `.../auth.service.ts`
  - Conventions: Injectable with `providedIn: 'root'`, use `environment.apiUrl`, manage state via signals, persist tokens through `TokenStorageService`, return Observables.
- **frontend-models**
  - Examples: `redum-frontend/src/app/core/models/task.model.ts`, `.../user.model.ts`
  - Conventions: Interface definitions mirroring backend payloads, union literal types for enums, optional fields allow `undefined` so spreads omit unset values.
- **frontend-auth-components**
  - Examples: `redum-frontend/src/app/features/auth/login/login.component.*`, `.../register/register.component.*`
  - Conventions: Standalone Angular Material forms with signals for loading state, display validation via `@if`, drive navigation/snack-bars through `AuthService`.
- **frontend-task-dashboard-components**
  - Examples: `redum-frontend/src/app/features/tasks/task-dashboard/task-dashboard.component.*`
  - Conventions: Standalone Kanban board using CDK drag-drop, computed signals for columns, dialogs for CRUD, snack-bar feedback, reload on failure.
- **frontend-shared-dialog-components**
  - Examples: `redum-frontend/src/app/shared/components/create-task-dialog/create-task-dialog.component.*`
  - Conventions: Standalone MatDialog forms, normalize Date/priority before closing, keep AI button disabled placeholder.
- **frontend-shared-task-card-components**
  - Examples: `redum-frontend/src/app/shared/components/task-card/task-card.component.*`
  - Conventions: Standalone Material cards accepting `task` input, emit `edit/delete` events, helper methods map priority to labels/colors.
- **frontend-layout-components**
  - Examples: `redum-frontend/src/app/shared/layout/main-layout/main-layout.component.*`
  - Conventions: Standalone layout with Material sidenav/toolbar, nav items defined as data array, logout through `AuthService`.
- **frontend-services** (already listed; ensure no duplication?) Already done above; keep as is.
- **frontend-environment-config**
  - Examples: `redum-frontend/src/environments/environment.ts`, `environment.prod.ts`
  - Conventions: Mirror object shape across environments, suffix URLs with `/api/v1`, toggle `production` boolean.

## 3. Feature Scaffold Guide
1. **Identify required categories** using the references above:
   - New API behavior → update/add files in `backend-api-routing`, `backend-use-cases`, `backend-repository-implementations`, optionally migrations/config.
   - New Angular UI feature → combine `frontend-app-configuration` (routes/providers), relevant feature component category, shared components, and services/models.
2. **Create backend artifacts** following clean architecture:
   - Add domain schema updates under `backend-domain-schemas`, ensure matching SQLAlchemy model if needed (`backend-domain-models`).
   - Extend repository interface/implementation to support new data access before modifying use case services.
   - Wire endpoints via a new or existing router with prefixed `APIRouter`, returning Pydantic read models.
3. **Create frontend artifacts** following standalone pattern:
   - Generate standalone component files (`*.component.ts/html/scss`) importing Angular Material modules.
   - Register routes using lazy `loadComponent` in `app.routes.ts` and guard them if protected.
   - Extend services with new API calls, updating signals in `tap` and sharing state via computed selectors.
   - Update shared models/interfaces so components and services stay in sync with backend responses.
4. **Place files consistently**:
   - Backend: domain logic in `app/domain`, use cases in `app/use_cases/<domain>`, repositories under `app/infrastructure/repositories`, endpoints in `app/api/v1/endpoints`.
   - Frontend: feature components under `src/app/features/<feature>`, shared UI under `src/app/shared`, core utilities/services under `src/app/core`.
5. **Naming and structure**:
   - Use descriptive filenames mirroring resource name (e.g., `reporting.py`, `report-dashboard.component.ts`).
   - Keep Angular SCSS and HTML files co-located with their TypeScript component.
   - Ensure new environment/config keys exist in both dev and prod files.

## 4. Integration Rules
- **Backend API**: All routes mount under `/api/v1`, use dependency-injected services with `Depends(get_db)`, and translate domain errors to `HTTPException` statuses.
- **Authentication**: Password hashing/verification must use `AuthService` (Passlib bcrypt); JWTs require HS256, `sub` claim, 60-minute expiration, and tokens validated via `AuthService.get_user_from_token`.
- **Tasks Domain**: Task status limited to `todo`/`in_progress`/`done`; TaskService enforces ownership before writes and only applies provided fields (partial updates via `model_dump(exclude_unset=True)`).
- **Data Layer**: Repositories are the sole access point for SQLAlchemy sessions; sessions come from `get_db`, and clean architecture boundaries forbid direct SQL in routes/use cases.
- **Configuration**: Read env values through `Settings`; new configurable behavior must use validators or typed fields.
- **Frontend Routing**: Routes load standalone components via `loadComponent`; authenticated sections require `authGuard` and fall back to `/tasks` on unknown paths.
- **Frontend State Management**: Services expose state as Angular signals; components derive computed views and must not mutate arrays in place—always update through service methods.
- **Frontend UI**: Material components, SCSS co-location, drag-and-drop operations rely on CDK; dialogs should normalize data before returning to services.
- **Auth Integration**: Token interceptor only tags `/api/v1/` calls; guard redirects preserve `returnUrl`; logout clears token via `TokenStorageService`.

Following these instructions keeps new features aligned with the existing FastAPI clean architecture and Angular standalone/Material patterns while maintaining consistency across backend and frontend layers.