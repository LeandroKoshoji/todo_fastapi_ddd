import pytest
from sqlalchemy.orm import Session
from app.core.user.domain.user import User, UserId
from app.core.user.infra.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository


@pytest.fixture
def user_repository(db_session: Session) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(db_session)


@pytest.mark.integration
def test_save_user(user_repository: SqlAlchemyUserRepository):
    user = User(username="testuser", email="testuser@email.com",
                hashed_password="hashed_password")
    user_repository.save_user(user)

    retrieved_user = user_repository.get_user_by_email(
        email="testuser@email.com")
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "testuser@email.com"
