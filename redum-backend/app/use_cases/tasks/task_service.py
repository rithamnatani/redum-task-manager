from typing import List
from app.domain.schemas.task import TaskCreate, TaskRead
from app.domain.interfaces.itask_repository import ITaskRepository


class TaskService:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def create_task(self, user_id: int, payload: TaskCreate) -> TaskRead:
        task = self.repo.create(task_create=payload, user_id=user_id)
        return TaskRead.from_orm(task)

    def get_user_tasks(self, user_id: int) -> List[TaskRead]:
        tasks = self.repo.get_all_by_user(user_id=user_id)
        return [TaskRead.from_orm(t) for t in tasks]
