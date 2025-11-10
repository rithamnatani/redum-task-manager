---
trigger: model_decision
description: When working on backend
---

FastAPI monolith architecture - NOT microservices
Clean Architecture: dependencies flow inwards (domain → use_cases → infrastructure → api)
Routes must be thin: parse → call one use case → return
No business logic in routes
Repository Pattern mandatory for all database operations
Always use FastAPI Depends for dependency injection
Separate SQLAlchemy models (domain/models/) from Pydantic schemas (domain/schemas/)

pydantic v1 only
python 3.11.9