from typing import List, Optional

from fastapi import HTTPException

from app.domain.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskSuggestionRead,
    TaskSuggestionRequest,
    TaskUpdate,
)
from app.domain.interfaces.itask_repository import ITaskRepository
from app.services.ai_service import RAGService, TaskSuggestion


class TaskService:
    def __init__(self, repo: ITaskRepository, rag_service: Optional[RAGService] = None):
        self.repo = repo
        self.rag_service = rag_service

    def create_task(self, user_id: int, payload: TaskCreate) -> TaskRead:
        task = self.repo.create(task_create=payload, user_id=user_id)
        task_read = TaskRead.model_validate(task, from_attributes=True)
        self._sync_task_to_kb(task_read)
        return task_read

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
        task_read = TaskRead.model_validate(updated_task, from_attributes=True)
        self._sync_task_to_kb(task_read)
        return task_read

    def delete_task(self, task_id: int, user_id: int) -> None:
        # Verify task exists and belongs to user
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")

        self.repo.delete(task_id)
        self._remove_task_from_kb(task_id)

    def suggest_task_metadata(
        self,
        *,
        user_id: int,
        payload: TaskSuggestionRequest,
    ) -> TaskSuggestionRead:
        if not self.rag_service:
            raise HTTPException(status_code=503, detail="Suggestions are not configured")

        suggestion: TaskSuggestion = self.rag_service.suggest_metadata(
            user_id=user_id,
            description=payload.description or "",
            title=payload.title,
            priority=payload.priority,
            status=payload.status,
        )
        suggestion_read = TaskSuggestionRead.model_validate(suggestion)
        suggestion_data = suggestion_read.model_dump()

        if payload.title:
            suggestion_data["title"] = None
        if payload.description:
            suggestion_data["description"] = None
        if payload.priority is not None:
            suggestion_data["priority"] = None
        if payload.status:
            suggestion_data["status"] = None

        return TaskSuggestionRead(**suggestion_data)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sync_task_to_kb(self, task: TaskRead) -> None:
        if not self.rag_service:
            return
        try:
            self.rag_service.add_task_to_kb(task)
        except ValueError:
            # Raised when configuration missing; treat as disabled
            pass

    def _remove_task_from_kb(self, task_id: int) -> None:
        if not self.rag_service:
            return
        self.rag_service.remove_task_from_kb(task_id)
