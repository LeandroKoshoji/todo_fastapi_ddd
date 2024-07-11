import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from app.core.task.domain.task import Task, TaskStatus

DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0


@dataclass
class SearchTaskFilters:
    user_id: uuid.UUID
    limit: int = DEFAULT_LIMIT
    offset: int = DEFAULT_OFFSET
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    send_notification: Optional[bool] = None


class TaskRepository(ABC):
    @abstractmethod
    def save_task(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task: Task) -> Task:
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_tasks_by_user_id(self, user_id: uuid.UUID) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def search_tasks(self, filters: SearchTaskFilters) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_task_by_id(self, task_id: uuid.UUID) -> Task | None:
        raise NotImplementedError
