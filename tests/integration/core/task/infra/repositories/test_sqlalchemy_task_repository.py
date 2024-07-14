import pytest
from sqlalchemy.orm import Session
from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import SearchTaskFilters
from app.core.task.infra.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from tests.helpers import create_task, create_user


@pytest.fixture
def task_repository(db_session: Session) -> SqlAlchemyTaskRepository:
    return SqlAlchemyTaskRepository(db_session)


@pytest.mark.integration
def test_save_task(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    user = create_user(db_session)
    task = Task(
        title="Test Task",
        description="Test Description",
        user_id=user.id,
        status="pending",
        send_notification=True
    )

    task_repository.save_task(task)

    retrieved_task = task_repository.get_task_by_id(task.id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.description == "Test Description"
    assert retrieved_task.user_id == user.id
    assert retrieved_task.status == "pending"
    assert retrieved_task.send_notification is True


@pytest.mark.integration
def test_update_task(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    task = create_task(db_session)

    task.title = "Updated Task"
    task.status = "done"
    task.description = "Updated Description"
    task.send_notification = False

    task_repository.update_task(task)

    retrieved_task = task_repository.get_task_by_id(task.id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Updated Task"
    assert retrieved_task.description == "Updated Description"
    assert retrieved_task.status == "done"
    assert retrieved_task.send_notification is False


@pytest.mark.integration
def test_delete_task(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    task = create_task(db_session)

    task_repository.delete_task(task.id)

    with pytest.raises(ValueError, match=f"Task with id {task.id} not found"):
        task_repository.get_task_by_id(task.id)


@pytest.mark.integration
def test_get_task_by_id(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    task = create_task(db_session)

    retrieved_task = task_repository.get_task_by_id(task.id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.description == "Test Description"
    assert retrieved_task.user_id == task.user_id
    assert retrieved_task.status == "pending"
    assert retrieved_task.send_notification is True


@pytest.mark.integration
def test_get_tasks_by_user_id(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    user = create_user(db_session)
    task1 = Task(
        title="Test Task 1",
        description="Test Description 1",
        user_id=user.id,
        status="pending",
        send_notification=True
    )
    task2 = Task(
        title="Test Task 2",
        description="Test Description 2",
        user_id=user.id,
        status="pending",
        send_notification=True
    )

    task_repository.save_task(task1)
    task_repository.save_task(task2)

    tasks_in_db = task_repository.get_tasks_by_user_id(user.id)

    assert len(tasks_in_db) == 2
    assert tasks_in_db[0].title == "Test Task 1"
    assert tasks_in_db[1].title == "Test Task 2"
    assert tasks_in_db[0].description == "Test Description 1"
    assert tasks_in_db[1].description == "Test Description 2"
    assert tasks_in_db[0].user_id == user.id
    assert tasks_in_db[1].user_id == user.id
    assert tasks_in_db[0].status == "pending"
    assert tasks_in_db[1].status == "pending"
    assert tasks_in_db[0].send_notification is True
    assert tasks_in_db[1].send_notification is True


@pytest.mark.integration
def test_search_tasks_should_return_all_user_tasks_when_filters_is_not_empty(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    task = create_task(db_session)

    filters = SearchTaskFilters(
        user_id=task.user_id,
        title=None,
        description=None,
        status=None,
        send_notification=None,
        offset=0,
        limit=10
    )

    tasks_in_db, total = task_repository.search_tasks(filters)

    assert total == 1
    assert len(tasks_in_db) == 1
    assert tasks_in_db[0].title == "Test Task"
    assert tasks_in_db[0].description == "Test Description"
    assert tasks_in_db[0].status == "pending"
    assert tasks_in_db[0].send_notification is True


@pytest.mark.integration
def test_search_tasks_should_return_empty_list_when_no_task_is_found(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    task = create_task(db_session)
    filters = SearchTaskFilters(
        user_id=task.user_id,
        title='Non existent task',
        description=None,
        status=None,
        send_notification=None,
        offset=0,
        limit=10
    )

    tasks_in_db, total = task_repository.search_tasks(filters)

    assert total == 0
    assert len(tasks_in_db) == 0
