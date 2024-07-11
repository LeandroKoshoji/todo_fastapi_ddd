from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import TaskRepository


class ListTaskByIdUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, task_id: str) -> Task:
        task = self.task_repository.get_task_by_id(task_id)
        return task
