from typing import List

from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import (
    SearchTaskFilters,
    TaskRepository,
)


class SearchTasksUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, filters: SearchTaskFilters) -> List[Task]:
        return self.task_repository.search_tasks(filters)
