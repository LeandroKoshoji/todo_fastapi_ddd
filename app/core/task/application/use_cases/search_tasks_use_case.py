from typing import List, Tuple

from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import (
    SearchTaskFilters,
    TaskRepository,
)


class SearchTasksUseCase:
    def __init__(
        self,
        task_repository: TaskRepository
    ) -> Tuple[List[Task], int]:
        self.task_repository = task_repository

    def execute(self, filters: SearchTaskFilters):
        tasks, total = self.task_repository.search_tasks(filters)
        return [t.to_dict() for t in tasks], total
