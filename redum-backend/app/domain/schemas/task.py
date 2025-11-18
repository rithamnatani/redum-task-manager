from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

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

    model_config = ConfigDict(from_attributes=True, validate_assignment=True)

    @field_validator("status", mode="before")
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

    @field_validator("title", "description", mode="before")
    def empty_str_to_none(cls, value: Optional[str]) -> Optional[str]:  # noqa: N805
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @model_validator(mode="after")
    def require_title_or_description(self) -> "TaskSuggestionRequest":  # noqa: N805
        if not self.title and not self.description:
            raise ValueError("Provide at least a title or description for suggestions")
        return self


class TaskSuggestionRead(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[TaskStatusType] = None

    model_config = ConfigDict(from_attributes=True)
