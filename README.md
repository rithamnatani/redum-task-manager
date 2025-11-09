# Redum Task Manager

A full-stack, AI-augmented task management platform showcasing senior-level engineering skills with modern web development practices.

## 🏗️ Architecture

This project follows **Clean Architecture** principles and consists of:

### Backend (`redum-backend/`)
- **Framework**: FastAPI with Python
- **Architecture**: Production-grade monolith (NOT microservices)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Authentication**: JWT with bcrypt
- **Migrations**: Alembic

### Frontend (`redum-frontend/`)
- **Framework**: Angular with TypeScript
- **Architecture**: SPA with CoreModule, SharedModule, FeatureModule pattern
- **State Management**: RxJS BehaviorSubjects (NO NgRx)
- **Forms**: Angular Reactive Forms

### Infrastructure (`redum-infra/`)
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Docker Compose for local development
- **Cloud**: AWS ECS + Fargate for production
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js (for frontend development)
- Python 3.11+ (for local backend development)

### Backend Development

```bash
cd redum-backend
docker-compose up --build
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432
- **Redis**: localhost:6379

### Frontend Development

```bash
cd redum-frontend
npm install
ng serve
```

The frontend will be available at http://localhost:4200

## 🧪 API Testing

This project includes Bruno API tests in the `api-tests/` directory:

1. Import the `api-tests` folder into Bruno
2. Select "Local Development" environment
3. Run tests in sequence:
   - Health Check
   - Register User
   - Login User
   - Create Task
   - List Tasks

## 📁 Project Structure

```
redum-task-manager/
├── .github/                 # GitHub workflows and templates
├── api-tests/               # Bruno API testing collection
├── redum-backend/           # FastAPI monolith
│   ├── app/
│   │   ├── api/v1/endpoints/    # Thin FastAPI routers
│   │   ├── use_cases/           # Business logic
│   │   ├── domain/
│   │   │   ├── models/          # SQLAlchemy models
│   │   │   ├── schemas/         # Pydantic DTOs
│   │   │   └── interfaces/      # Abstract interfaces
│   │   ├── infrastructure/
│   │   │   ├── database/        # DB session management
│   │   │   ├── repositories/    # Concrete implementations
│   │   │   ├── services/        # External API clients
│   │   │   └── cache/           # Redis setup
│   │   └── core/                # Configuration
│   ├── alembic/             # Database migrations
│   ├── docker-compose.yml   # Local development
│   └── backend.Dockerfile   # Production build
├── redum-frontend/          # Angular SPA
├── redum-infra/             # Infrastructure as code
└── redum-docs/              # Documentation
```

## 🏛️ Architecture Principles

### Backend (Clean Architecture)
1. **Dependencies flow inwards**: Domain → Use Cases → Infrastructure → API
2. **Thin Controllers**: Routes only parse requests and call use cases
3. **Repository Pattern**: All database operations abstracted through interfaces
4. **Dependency Injection**: FastAPI's `Depends` system throughout
5. **Separation of Concerns**: Models (DB) vs Schemas (API)

### Frontend (Angular Best Practices)
1. **Modular Architecture**: CoreModule, SharedModule, FeatureModules
2. **Singleton Services**: AuthService, TaskService in CoreModule
3. **Reactive State Management**: RxJS BehaviorSubjects
4. **Type Safety**: TypeScript throughout
5. **Form Handling**: Reactive Forms for all user input

## 🛠️ Development Workflow

### Backend Development
1. Define interfaces in `domain/interfaces/`
2. Create SQLAlchemy models in `domain/models/`
3. Create Pydantic schemas in `domain/schemas/`
4. Implement repositories in `infrastructure/repositories/`
5. Create services in `use_cases/`
6. Build thin endpoints in `api/v1/endpoints/`

### Database Migrations
```bash
cd redum-backend
docker-compose exec backend alembic revision --autogenerate -m "Description"
docker-compose exec backend alembic upgrade head
```

### API Testing
Use Bruno collection in `api-tests/` directory for comprehensive API testing.

## 🔧 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secure-secret-key
```

## 📊 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Pydantic**: Data validation using Python type annotations
- **PostgreSQL**: Powerful, open source object-relational database
- **Redis**: In-memory data structure store
- **JWT**: JSON Web Tokens for authentication

### Frontend
- **Angular**: Platform for building mobile and desktop web applications
- **TypeScript**: Typed superset of JavaScript
- **RxJS**: Reactive extensions for JavaScript
- **Angular Material**: UI component library

### DevOps
- **Docker**: Platform for developing, shipping, and running applications
- **GitHub Actions**: CI/CD platform
- **AWS ECS**: Scalable container orchestration
- **Bruno**: API testing platform

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

- **Ritham Natani** - [@rithamnatani](https://github.com/rithamnatani)

---

⭐ If this project helps you, please give it a star!
