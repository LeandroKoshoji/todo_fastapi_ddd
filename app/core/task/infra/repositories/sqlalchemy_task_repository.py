from sqlalchemy.orm import Session

from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import TaskRepository
from app.core.task.infra.models.task_model import Task as TaskModel


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_task(self, task: Task) -> Task:
        task_model = TaskModel(
            id=task.id,
            title=task.title,
            user_id=task.user_id,
            status=task.status,
            description=task.description,
            send_notification=task.send_notification
        )
        self.db.add(task_model)
        self.db.commit()
        self.db.refresh(task_model)
        return self._map_to_domain(task_model)

    def _map_to_domain(self, task_model: TaskModel) -> Task:
        return Task(
            id=task_model.id,
            title=task_model.title,
            user_id=task_model.user_id,
            status=task_model.status,
            description=task_model.description,
            send_notification=task_model.send_notification,
            created_at=task_model.created_at
        )
