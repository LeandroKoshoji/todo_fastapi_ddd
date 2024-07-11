from app.core.task.domain.commands.edit_task_command import EditTaskCommand
from app.core.task.domain.events.task_edited_event import TaskEditedEvent
from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import TaskRepository


class EditTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, command: EditTaskCommand) -> TaskEditedEvent:
        task = Task(
            id=command.id,
            title=command.title,
            user_id=command.user_id,
            status=command.status,
            description=command.description,
            send_notification=command.send_notification
        )

        edited_task = self.task_repository.update_task(task)
        return TaskEditedEvent(**edited_task.to_dict())
