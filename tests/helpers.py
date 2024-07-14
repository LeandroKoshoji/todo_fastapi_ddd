from sqlalchemy.orm import Session
from app.core.user.domain.user import User, UserId
from app.core.user.infra.models.user_model import User as UserModel


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
