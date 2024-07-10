from app.core.task.domain.commands.create_task_command import CreateTaskCommand
from app.core.task.domain.events.task_created_event import TaskCreatedEvent
from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import TaskRepository


class CreateTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, command: CreateTaskCommand) -> TaskCreatedEvent:
        task = Task(
            title=command.title,
            user_id=command.user_id,
            status=command.status,
            description=command.description,
            send_notification=command.send_notification
        )

        task_db = self.task_repository.save_task(task)

        return TaskCreatedEvent(
            **task_db.to_dict()
        )
