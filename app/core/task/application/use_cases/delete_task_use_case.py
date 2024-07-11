from app.core.task.domain.commands.delete_task_command import DeleteTaskCommand
from app.core.task.domain.events.task_deleted_event import TaskDeletedEvent
from app.core.task.domain.task_repository import TaskRepository


class DeleteTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, command: DeleteTaskCommand) -> TaskDeletedEvent:
        self.task_repository.delete_task(command.id)
        return TaskDeletedEvent()
