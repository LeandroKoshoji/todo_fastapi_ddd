from typing import List

from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import TaskRepository


class ListAllTasksByUserUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, user_id: str) -> List[Task]:
        task = self.task_repository.get_tasks_by_user_id(user_id)
        return [t.to_dict() for t in task]
