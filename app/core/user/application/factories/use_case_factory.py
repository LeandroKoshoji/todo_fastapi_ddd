from sqlalchemy.orm import Session

from app.core.shared.security.jwt import JWTService
from app.core.shared.security.password_hasher import PasswordHasher
from app.core.user.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from app.core.user.application.use_cases.login_user_use_case import (
    LoginUserUseCase,
)
from app.core.user.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


def create_create_user_use_case(db: Session) -> CreateUserUseCase:
    password_hasher = PasswordHasher()
    user_repository = SqlAlchemyUserRepository(db)
    return CreateUserUseCase(user_repository, password_hasher)


def create_login_user_use_case(db: Session) -> LoginUserUseCase:
    password_hasher = PasswordHasher()
    user_repository = SqlAlchemyUserRepository(db)
    jwt_service = JWTService()
    return LoginUserUseCase(user_repository, password_hasher, jwt_service)
