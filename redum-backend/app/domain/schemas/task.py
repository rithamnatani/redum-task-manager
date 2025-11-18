from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, validator, root_validator

from app.domain.models.task import TaskStatus

# Type alias for task status
TaskStatusType = Literal["todo", "in_progress", "done"]


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    status: Optional[TaskStatusType] = "todo"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    status: Optional[TaskStatusType] = None


class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    priority: Optional[int]
    status: Union[TaskStatusType, TaskStatus]
    user_id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
        use_enum_values = True

    @validator("status", pre=True, always=True)
    def serialize_status(
        cls, value: Union[TaskStatusType, TaskStatus]
    ) -> TaskStatusType:
        if isinstance(value, TaskStatus):
            return value.value
        return value


class TaskSuggestionRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[TaskStatusType] = None

    @validator("title", "description", pre=True)
    def empty_str_to_none(cls, value: Optional[str]) -> Optional[str]:  # noqa: N805
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @root_validator
    def require_title_or_description(cls, values: dict[str, Optional[str]]) -> dict[str, Optional[str]]:  # noqa: N805
        if not values.get("title") and not values.get("description"):
            raise ValueError("Provide at least a title or description for suggestions")
        return values


class TaskSuggestionRead(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[TaskStatusType] = None
