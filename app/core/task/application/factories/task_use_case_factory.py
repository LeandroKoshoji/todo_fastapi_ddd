from sqlalchemy.orm import Session

from app.core.task.application.use_cases.create_task_use_case import (
    CreateTaskUseCase,
)
from app.core.task.application.use_cases.delete_task_use_case import (
    DeleteTaskUseCase,
)
from app.core.task.application.use_cases.edit_task_use_case import (
    EditTaskUseCase,
)
from app.core.task.application.use_cases.list_all_tasks_by_user_use_case import (
    ListAllTasksByUserUseCase,
)
from app.core.task.application.use_cases.list_task_by_id_use_case import (
    ListTaskByIdUseCase,
)
from app.core.task.application.use_cases.search_tasks_use_case import (
    SearchTasksUseCase,
)
from app.core.task.infra.repositories.sqlalchemy_task_repository import (
    SqlAlchemyTaskRepository,
)


def create_task_use_case_factory(db: Session) -> CreateTaskUseCase:
    task_repository = SqlAlchemyTaskRepository(db)
    return CreateTaskUseCase(task_repository)


def edit_task_use_case_factory(db: Session) -> EditTaskUseCase:
    task_repository = SqlAlchemyTaskRepository(db)
    return EditTaskUseCase(task_repository)


def delete_task_use_case_factory(db: Session) -> DeleteTaskUseCase:
    task_repository = SqlAlchemyTaskRepository(db)
    return DeleteTaskUseCase(task_repository)


def search_tasks_use_case_factory(db: Session) -> SearchTasksUseCase:
    task_repository = SqlAlchemyTaskRepository(db)
    return SearchTasksUseCase(task_repository)


def list_all_tasks_by_user_use_case_factory(db: Session) -> ListAllTasksByUserUseCase:
    task_repository = SqlAlchemyTaskRepository(db)
    return ListAllTasksByUserUseCase(task_repository)


def list_task_by_id_use_case_factory(db: Session) -> ListTaskByIdUseCase:
    task_repository = SqlAlchemyTaskRepository(db)
    return ListTaskByIdUseCase(task_repository)
