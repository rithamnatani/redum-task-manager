from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.interfaces.itask_repository import ITaskRepository
from app.domain.schemas.task import TaskCreate
from app.domain.models.task import Task


class TaskRepository(ITaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, *, task_create: TaskCreate, user_id: int) -> Task:
        task = Task(
            title=task_create.title,
            description=task_create.description,
            due_date=task_create.due_date,
            priority=task_create.priority,
            status=task_create.status,
            user_id=user_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all_by_user(self, user_id: int) -> List[Task]:
        return self.db.query(Task).filter(Task.user_id == user_id).all()

    def update(self, task_id: int, **fields) -> Task:
        task = self.get_by_id(task_id)
        if not task:
            return None
        for k, v in fields.items():
            setattr(task, k, v)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)
        if task:
            self.db.delete(task)
            self.db.commit()
