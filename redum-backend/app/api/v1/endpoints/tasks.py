from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.domain.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.use_cases.tasks.task_service import TaskService
from app.infrastructure.database.session import get_db
from sqlalchemy.orm import Session
from app.infrastructure.repositories.task_repository import TaskRepository
from fastapi.security import OAuth2PasswordBearer
from app.use_cases.auth.auth_service import AuthService
from app.infrastructure.repositories.user_repository import UserRepository

router = APIRouter(prefix="/tasks", tags=["tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    repo = TaskRepository(db)
    return TaskService(repo)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = UserRepository(db)
    return AuthService(repo)


def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
) -> int:
    try:
        user = auth_service.get_user_from_token(token)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return user.id


@router.post("/", response_model=TaskRead)
def create_task(
    payload: TaskCreate,
    svc: TaskService = Depends(get_task_service),
    user_id: int = Depends(get_current_user_id),
):
    return svc.create_task(user_id=user_id, payload=payload)


@router.get("/", response_model=List[TaskRead])
def list_tasks(
    svc: TaskService = Depends(get_task_service),
    user_id: int = Depends(get_current_user_id),
):
    return svc.get_user_tasks(user_id=user_id)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    svc: TaskService = Depends(get_task_service),
    user_id: int = Depends(get_current_user_id),
):
    return svc.update_task(task_id=task_id, user_id=user_id, payload=payload)


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    svc: TaskService = Depends(get_task_service),
    user_id: int = Depends(get_current_user_id),
):
    svc.delete_task(task_id=task_id, user_id=user_id)
    return None
