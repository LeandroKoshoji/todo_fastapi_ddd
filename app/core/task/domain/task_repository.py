from abc import ABC, abstractmethod
import uuid

from app.core.task.domain.task import Task


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
    # @abstractmethod
    # def get_task_by_id(self, task_id: str) -> Task | None:
    #     raise NotImplementedError

    # @abstractmethod
    # def get_all_tasks(self) -> list[Task]:
    #     raise NotImplementedError
