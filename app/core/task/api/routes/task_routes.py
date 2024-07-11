from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pytest import Session

from app.core.shared.application.utils import success_response
from app.core.shared.infrastructure.database.database import get_db
from app.core.shared.security.dependecies import get_current_user
from app.core.task.application.use_cases.create_task_use_case import (
    CreateTaskUseCase,
)
from app.core.task.application.use_cases.delete_task_use_case import DeleteTaskUseCase
from app.core.task.application.use_cases.edit_task_use_case import EditTaskUseCase
from app.core.task.domain.commands.create_task_command import CreateTaskCommand
from app.core.task.domain.commands.delete_task_command import DeleteTaskCommand
from app.core.task.domain.commands.edit_task_command import EditTaskCommand
from app.core.task.domain.exceptions import InvalidDomainRuleError
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
