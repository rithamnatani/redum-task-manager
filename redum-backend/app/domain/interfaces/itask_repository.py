from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.task import Task
from app.domain.schemas.task import TaskCreate


class ITaskRepository(ABC):
    @abstractmethod
    def create(self, *, task_create: TaskCreate, user_id: int) -> Task:
        ...

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        ...

    @abstractmethod
    def get_all_by_user(self, user_id: int) -> List[Task]:
        ...

    @abstractmethod
    def update(self, task_id: int, **fields) -> Task:
        ...

    @abstractmethod
    def delete(self, task_id: int) -> None:
        ...
