import pytest
from sqlalchemy.orm import Session
from app.core.user.domain.user import User, UserId
from app.core.user.infra.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository
)
from tests.helpers import create_user


@pytest.fixture
def user_repository(db_session: Session) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(db_session)


@pytest.mark.integration
def test_save_user(
    user_repository: SqlAlchemyUserRepository,
    db_session: Session
):
    user_id = UserId()
    user = User(
        id=user_id.id,
        username="testuser",
        email="testuser@email.com",
        hashed_password="hashed_password"
    )
    user_repository.save_user(user)

    retrieved_user = user_repository.get_user_by_id(user_id.id)
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "testuser@email.com"


@pytest.mark.integration
def test_get_user_by_id(
    user_repository: SqlAlchemyUserRepository,
    db_session: Session
):
    user_id = create_user(db_session)
    retrieved_user = user_repository.get_user_by_id(user_id.id)

    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "testuser@email.com"


@pytest.mark.integration
def test_get_user_by_email(
    user_repository: SqlAlchemyUserRepository,
    db_session: Session
):
    create_user(db_session)
    retrieved_user = user_repository.get_user_by_email("testuser@email.com")

    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "testuser@email.com"


@pytest.mark.integration
def test_delete_user(
    user_repository: SqlAlchemyUserRepository,
    db_session: Session
):
    user_id = create_user(db_session).id
    user_repository.delete_user(user_id)

    retrieved_user = user_repository.get_user_by_id(user_id)
    assert retrieved_user is None
