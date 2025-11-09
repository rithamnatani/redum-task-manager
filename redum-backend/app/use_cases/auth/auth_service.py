from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from app.domain.schemas.user import UserCreate, UserRead
from app.domain.schemas.token import Token
from app.infrastructure.repositories.user_repository import UserRepository
from app.core.config import Settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = Settings()


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def _verify_password(self, plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

    def register_user(self, payload: UserCreate) -> UserRead:
        existing = self.repo.get_by_email(payload.email)
        if existing:
            raise ValueError("email already registered")
        hashed = self._hash_password(payload.password)
        user = self.repo.create(email=payload.email, hashed_password=hashed)
        return UserRead.model_validate(user)

    def login_for_access_token(self, email: str, password: str) -> Token:
        user = self.repo.get_by_email(email)
        if not user or not self._verify_password(password, user.hashed_password):
            raise ValueError("invalid credentials")

        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
        to_encode = {"sub": str(user.id), "exp": expire}
        access_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return Token(access_token=access_token, token_type="bearer")
