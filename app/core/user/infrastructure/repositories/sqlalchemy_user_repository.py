from sqlalchemy.orm import Session

from app.core.user.domain.user import User, UserId
from app.core.user.domain.user_repository import UserRepository
from app.core.user.infrastructure.models.user_model import User as UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: UserId) -> User | None:
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def save_user(self, user: User) -> None:
        db_user = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
        )
        self.db.add(db_user)
        self.db.commit()

    def delete_user(self, user_id: UserId) -> None:
        self.db.query(UserModel).filter(UserModel.id == user_id).delete()
        self.db.commit()

    def get_user_by_email(self, email: str) -> User | None:
        return (
            self.db.query(UserModel).filter(UserModel.email == email).first()
        )
