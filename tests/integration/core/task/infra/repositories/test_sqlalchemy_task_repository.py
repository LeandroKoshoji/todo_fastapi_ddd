import pytest
from sqlalchemy.orm import Session
from app.core.task.domain.task import Task
from app.core.task.domain.task_repository import SearchTaskFilters
from app.core.task.infra.repositories.sqlalchemy_task_repository import SqlAlchemyTaskRepository
from tests.helpers import create_tasks, create_user


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
    task = create_tasks(db_session)[0]

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
    task = create_tasks(db_session)[0]

    task_repository.delete_task(task.id)

    with pytest.raises(ValueError, match=f"Task with id {task.id} not found"):
        task_repository.get_task_by_id(task.id)


@pytest.mark.integration
def test_get_task_by_id(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    task = create_tasks(db_session)[0]

    retrieved_task = task_repository.get_task_by_id(task.id)
    assert retrieved_task is not None
    assert retrieved_task.title == "Test Task 1"
    assert retrieved_task.description == "Test Description 1"
    assert retrieved_task.user_id == task.user_id
    assert retrieved_task.status == "pending"
    assert retrieved_task.send_notification is True


@pytest.mark.integration
def test_get_tasks_by_user_id(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    user = create_user(db_session)
    create_tasks(db_session, 10, user_id=user.id)

    tasks_in_db = task_repository.get_tasks_by_user_id(user.id)

    assert len(tasks_in_db) == 10
    for i, task in enumerate(tasks_in_db):
        assert task.title == f"Test Task {i+1}"
        assert task.description == f"Test Description {i+1}"
        assert task.user_id == user.id
        assert task.status == "pending"
        assert task.send_notification is True


@pytest.mark.integration
def test_search_tasks_should_return_all_user_tasks_when_filters_is_not_empty(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    user = create_user(db_session)
    create_tasks(
        db_session,
        2,
        user_id=user.id,
        status="pending"
    )
    create_tasks(
        db_session,
        2,
        user_id=user.id,
        status="on_going"
    )
    create_tasks(
        db_session,
        2,
        user_id=user.id,
        status="done"
    )

    filters = SearchTaskFilters(
        user_id=user.id,
        title=None,
        description=None,
        status=None,
        send_notification=None,
        offset=0,
        limit=10
    )

    tasks_in_db, total = task_repository.search_tasks(filters)

    pending_tasks = [task for task in tasks_in_db if task.status == "pending"]
    ongoing_tasks = [task for task in tasks_in_db if task.status == "on_going"]
    done_tasks = [task for task in tasks_in_db if task.status == "done"]

    assert total == 6
    assert len(tasks_in_db) == 6
    assert len(pending_tasks) == 2
    assert len(ongoing_tasks) == 2
    assert len(done_tasks) == 2


@pytest.mark.integration
def test_search_tasks_should_return_empty_list_when_no_task_is_found(
    task_repository: SqlAlchemyTaskRepository,
    db_session: Session
):
    task = create_tasks(db_session)[0]
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
