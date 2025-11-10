from fastapi import APIRouter, Depends
from typing import List
from app.domain.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.use_cases.tasks.task_service import TaskService
from app.infrastructure.database.session import get_db
from sqlalchemy.orm import Session
from app.infrastructure.repositories.task_repository import TaskRepository

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    repo = TaskRepository(db)
    return TaskService(repo)


@router.post("/", response_model=TaskRead)
def create_task(payload: TaskCreate, svc: TaskService = Depends(get_task_service)):
    # In a real app, user_id would be resolved from the auth token
    user_id = 1
    return svc.create_task(user_id=user_id, payload=payload)


@router.get("/", response_model=List[TaskRead])
def list_tasks(svc: TaskService = Depends(get_task_service)):
    user_id = 1
    return svc.get_user_tasks(user_id=user_id)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate, svc: TaskService = Depends(get_task_service)):
    # In a real app, user_id would be resolved from the auth token
    user_id = 1
    return svc.update_task(task_id=task_id, user_id=user_id, payload=payload)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, svc: TaskService = Depends(get_task_service)):
    # In a real app, user_id would be resolved from the auth token
    user_id = 1
    svc.delete_task(task_id=task_id, user_id=user_id)
    return None
