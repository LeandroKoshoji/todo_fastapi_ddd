from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import TaskRepository
from app.core.task.infra.models.task_model import Task as TaskModel


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def save_task(self, task: Task) -> Task:
        try:
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
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update_task(self, task: Task) -> Task:
        try:
            task_model = self.db.query(TaskModel).filter_by(id=task.id).first()
            task_model.title = task.title
            task_model.status = task.status
            task_model.description = task.description
            task_model.send_notification = task.send_notification
            self.db.commit()
            return self._map_to_domain(task_model)
        except NoResultFound as e:
            raise ValueError(f"Task with id {task.id} not found")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

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
