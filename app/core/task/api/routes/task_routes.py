from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.core.shared.application.schemas.response import (
    PaginatedResponseModel,
    ResponseModel,
)
from app.core.shared.application.utils import (
    paginated_response,
    success_response,
)
from app.core.shared.infra.database.database import get_db
from app.core.shared.security.dependecies import get_current_user
from app.core.task.api.schemas.task_schemas import (
    CreateTaskResponseModel,
    CreateTaskSchema,
    EditTaskResponseModel,
    EditTaskSchema,
    ListTaskByIdResponseModel,
)
from app.core.task.application.factories.task_use_case_factory import (
    create_task_use_case_factory,
    delete_task_use_case_factory,
    edit_task_use_case_factory,
    list_all_tasks_by_user_use_case_factory,
    list_task_by_id_use_case_factory,
    search_tasks_use_case_factory,
)
from app.core.task.domain.commands.create_task_command import CreateTaskCommand
from app.core.task.domain.commands.delete_task_command import DeleteTaskCommand
from app.core.task.domain.commands.edit_task_command import EditTaskCommand
from app.core.task.domain.exceptions import InvalidDomainRuleError
from app.core.task.domain.task import TaskStatus
from app.core.task.domain.task_repository import SearchTaskFilters

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseModel[CreateTaskResponseModel],
    status_code=status.HTTP_201_CREATED
)
def create_task(
    input: CreateTaskSchema,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    use_case = create_task_use_case_factory(db)

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


@router.put(
    "/{task_id}",
    response_model=ResponseModel[EditTaskResponseModel],
    status_code=status.HTTP_200_OK
)
def edit_task(
    task_id: str,
    input: EditTaskSchema,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    use_case = edit_task_use_case_factory(db)

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


@router.delete(
    "/{task_id}",
    response_model=ResponseModel[None],
    status_code=status.HTTP_200_OK
)
def delete_task(
    task_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    use_case = delete_task_use_case_factory(db)
    command = DeleteTaskCommand(id=task_id)
    try:
        use_case.execute(command)
        return success_response(None, "Task deleted successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    '/search',
    response_model=PaginatedResponseModel[ListTaskByIdResponseModel],
    status_code=status.HTTP_200_OK
)
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
    use_case = search_tasks_use_case_factory(db)

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


@router.get(
    "/",
    response_model=ResponseModel[List[ListTaskByIdResponseModel]],
    status_code=status.HTTP_200_OK
)
def list_all_tasks(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    use_case = list_all_tasks_by_user_use_case_factory(db)

    try:
        tasks = use_case.execute(current_user.get("id"))
        return success_response(tasks, "Tasks retrieved successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{task_id}",
    response_model=ResponseModel[ListTaskByIdResponseModel],
    status_code=status.HTTP_200_OK
)
def list_task_by_id(
    task_id: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    use_case = list_task_by_id_use_case_factory(db)

    try:
        task = use_case.execute(task_id)
        return success_response(task, "Task retrieved successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
