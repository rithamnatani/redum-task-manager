from datetime import datetime
from typing import Literal, Optional, Union

from pydantic import BaseModel, validator

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
