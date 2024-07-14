import uuid

from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import (
    SearchTaskFilters,
    TaskRepository,
)
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
            return SqlAlchemyTaskRepository._map_to_domain(task_model)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update_task(self, task: Task) -> Task:
        try:
            task_model = self.db.query(TaskModel).filter_by(id=task.id).one()
            task_model.title = task.title
            task_model.status = task.status
            task_model.description = task.description
            task_model.send_notification = task.send_notification
            self.db.commit()
            return SqlAlchemyTaskRepository._map_to_domain(task_model)
        except NoResultFound:
            raise ValueError(f"Task with id {task.id} not found")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_task(self, task_id: uuid.UUID) -> None:
        try:
            task_model = self.db.query(TaskModel).filter_by(id=task_id).one()
            self.db.delete(task_model)
            self.db.commit()
        except NoResultFound:
            raise ValueError(f"Task with id {task_id} not found")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_task_by_id(self, task_id: uuid.UUID) -> Task:
        try:
            task_model = self.db.query(TaskModel).filter_by(id=task_id).one()
            return SqlAlchemyTaskRepository._map_to_domain(task_model)
        except NoResultFound:
            raise ValueError(f"Task with id {task_id} not found")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_tasks_by_user_id(self, user_id: uuid.UUID) -> list[Task]:
        task_models = self.db.query(TaskModel).filter_by(user_id=user_id).all()
        return [SqlAlchemyTaskRepository._map_to_domain(task_model) for task_model in task_models]

    def search_tasks(self, filters: SearchTaskFilters) -> list[Task]:
        query = self.db.query(TaskModel).filter_by(user_id=filters.user_id)
        if filters.title:
            query = query.filter(TaskModel.title.ilike(f"%{filters.title}%"))
        if filters.description:
            query = query.filter(TaskModel.description.ilike(
                f"%{filters.description}%"))
        if filters.status:
            query = query.filter(TaskModel.status == filters.status)
        if filters.send_notification is not None:
            query = query.filter(
                TaskModel.send_notification == filters.send_notification)
        total = query.count()
        task_models = query.offset(filters.offset).limit(filters.limit).all()
        return [
            SqlAlchemyTaskRepository._map_to_domain(task_model) for task_model in task_models
        ], total

    @staticmethod
    def _map_to_domain(task_model: TaskModel) -> Task:
        return Task(
            id=task_model.id,
            title=task_model.title,
            user_id=task_model.user_id,
            status=task_model.status,
            description=task_model.description,
            send_notification=task_model.send_notification,
            created_at=task_model.created_at
        )
