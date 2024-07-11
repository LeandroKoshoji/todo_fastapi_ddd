from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from pydantic import BaseModel
from pytest import Session

from app.core.shared.application.utils import paginated_response, success_response
from app.core.shared.infrastructure.database.database import get_db
from app.core.shared.security.dependecies import get_current_user
from app.core.task.application.use_cases.create_task_use_case import (
    CreateTaskUseCase,
)
from app.core.task.application.use_cases.delete_task_use_case import DeleteTaskUseCase
from app.core.task.application.use_cases.edit_task_use_case import EditTaskUseCase
from app.core.task.application.use_cases.list_all_tasks_by_user_use_case import ListAllTasksByUserUseCase
from app.core.task.application.use_cases.search_tasks_use_case import SearchTasksUseCase
from app.core.task.domain.commands.create_task_command import CreateTaskCommand
from app.core.task.domain.commands.delete_task_command import DeleteTaskCommand
from app.core.task.domain.commands.edit_task_command import EditTaskCommand
from app.core.task.domain.exceptions import InvalidDomainRuleError
from app.core.task.domain.task import TaskStatus
from app.core.task.domain.task_repository import SearchTaskFilters
from app.core.task.infra.repositories.sqlalchemy_task_repository import (
    SqlAlchemyTaskRepository,
)

router = APIRouter()


class CreateTaskSchema(BaseModel):
    title: str
    status: str
    description: str
    send_notification: bool


@router.post("/")
def create_task(input: CreateTaskSchema, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_repository = SqlAlchemyTaskRepository(db)
    use_case = CreateTaskUseCase(task_repository)

    command = CreateTaskCommand(
        title=input.title,
        user_id=current_user.get("id"),
        status=input.status,
        description=input.description,
        send_notification=input.send_notification
    )

    try:
        event = use_case.execute(command)
        return success_response(event, "Task created successfully")
    except InvalidDomainRuleError as e:
        raise HTTPException(status_code=400, detail=str(e.message))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{task_id}", status_code=200)
def edit_task(task_id: str, input: CreateTaskSchema, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_repository = SqlAlchemyTaskRepository(db)
    use_case = EditTaskUseCase(task_repository)

    command = EditTaskCommand(
        id=task_id,
        title=input.title,
        user_id=current_user.get("id"),
        status=input.status,
        description=input.description,
        send_notification=input.send_notification
    )

    try:
        event = use_case.execute(command)
        return success_response(event, "Task edited successfully")
    except InvalidDomainRuleError as e:
        raise HTTPException(status_code=400, detail=str(e.message))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task_repository = SqlAlchemyTaskRepository(db)
    use_case = DeleteTaskUseCase(task_repository)
    command = DeleteTaskCommand(id=task_id)
    try:
        use_case.execute(command)
        return success_response(None, "Task deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def list_all_tasks(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    task_repository = SqlAlchemyTaskRepository(db)
    use_case = ListAllTasksByUserUseCase(task_repository)

    try:
        tasks = use_case.execute(current_user.get("id"))
        return success_response(tasks, "Tasks retrieved successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/search')
def search_tasks(
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    send_notification: Optional[bool] = Query(None),
    page: int = Query(1, gt=0),
    per_page: int = Query(10, gt=0),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task_repository = SqlAlchemyTaskRepository(db)
    use_case = SearchTasksUseCase(task_repository)

    limit = per_page
    offset = (page - 1) * per_page

    filters = SearchTaskFilters(
        user_id=current_user.get("id"),
        limit=limit,
        offset=offset,
        title=title,
        description=description,
        status=status,
        send_notification=send_notification,
    )
    try:
        tasks, total = use_case.execute(filters)

        return paginated_response(
            tasks,
            "Tasks retrieved successfully",
            page=page,
            per_page=per_page,
            total=total,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
