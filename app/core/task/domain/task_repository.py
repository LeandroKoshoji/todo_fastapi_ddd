from abc import ABC

from app.core.task.domain.task import Task


class TaskRepository(ABC):
    def save_task(self, task: Task) -> Task:
        raise NotImplementedError

    def update_task(self, task: Task) -> Task:
        raise NotImplementedError

    def get_task_by_id(self, task_id: str) -> Task | None:
        raise NotImplementedError

    def delete_task(self, task_id: str) -> None:
        raise NotImplementedError

    def get_all_tasks(self) -> list[Task]:
        raise NotImplementedError

    def get_tasks_by_user_id(self, user_id: str) -> list[Task]:
        raise NotImplementedError
