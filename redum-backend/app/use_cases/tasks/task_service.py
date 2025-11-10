from typing import List
from app.domain.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.domain.interfaces.itask_repository import ITaskRepository
from fastapi import HTTPException


class TaskService:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def create_task(self, user_id: int, payload: TaskCreate) -> TaskRead:
        task = self.repo.create(task_create=payload, user_id=user_id)
        return TaskRead.model_validate(task, from_attributes=True)

    def get_user_tasks(self, user_id: int) -> List[TaskRead]:
        tasks = self.repo.get_all_by_user(user_id=user_id)
        return [TaskRead.model_validate(task, from_attributes=True) for task in tasks]

    def update_task(self, task_id: int, user_id: int, payload: TaskUpdate) -> TaskRead:
        # Verify task exists and belongs to user
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        # Only update fields that are provided
        update_data = payload.model_dump(exclude_unset=True)
        if not update_data:
            return TaskRead.model_validate(task, from_attributes=True)

        updated_task = self.repo.update(task_id, **update_data)
        return TaskRead.model_validate(updated_task, from_attributes=True)

    def delete_task(self, task_id: int, user_id: int) -> None:
        # Verify task exists and belongs to user
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")

        self.repo.delete(task_id)
