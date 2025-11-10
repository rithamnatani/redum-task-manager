from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import auth, tasks
from app.infrastructure.database.session import engine
from app.infrastructure.database.base import Base
from app.core.config import Settings


settings = Settings()


def create_app() -> FastAPI:
    app = FastAPI(title="redum-backend")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200"],  # Angular default port
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include routers under API version
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(tasks.router, prefix="/api/v1")

    @app.on_event("startup")
    def on_startup():
        # Create tables for quick local testing (use alembic for production)
        Base.metadata.create_all(bind=engine)

    return app


app = create_app()
