from sqlalchemy.orm import Session
from app.core.task.domain.task import Task, TaskId
from app.core.user.domain.user import User, UserId
from app.core.user.infra.models.user_model import User as UserModel
from app.core.task.infra.models.task_model import Task as TaskModel


def create_user(
    db_session: Session,
        user_id: str = None,
        username: str = "testuser",
        email: str = "testuser@email.com",
        hashed_password: str = "hashed_password"
) -> User:
    if user_id is None:
        user_id = UserId().id
    user = User(
        id=user_id,
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db_user = UserModel(
        id=user.id,
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password
    )
    db_session.add(db_user)
    db_session.commit()
    return user


def create_task(
    db_session: Session,
    task_id: str = None,
    title: str = "Test Task",
    description: str = "Test Description",
    user_id: str = None,
    status: str = "pending",
    send_notification: bool = True
) -> Task:
    if task_id is None:
        task_id = TaskId().id
    if user_id is None:
        user_id = create_user(db_session).id

    task = Task(
        id=task_id,
        title=title,
        description=description,
        user_id=user_id,
        status=status,
        send_notification=send_notification
    )
    db_task = TaskModel(
        id=task.id,
        title=task.title,
        user_id=task.user_id,
        status=task.status,
        description=task.description,
        send_notification=task.send_notification
    )
    db_session.add(db_task)
    db_session.commit()
    return task
