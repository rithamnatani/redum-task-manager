from fastapi import APIRouter, Depends, HTTPException
from app.domain.schemas.user import UserCreate, UserRead
from app.domain.schemas.token import Token
from app.use_cases.auth.auth_service import AuthService
from app.infrastructure.database.session import get_db
from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)


@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, svc: AuthService = Depends(get_auth_service)):
    try:
        return svc.register_user(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/token", response_model=Token)
def login(email: str, password: str, svc: AuthService = Depends(get_auth_service)):
    try:
        return svc.login_for_access_token(email=email, password=password)
    except Exception as exc:
        raise HTTPException(status_code=401, detail=str(exc))
