from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.shared.application.schemas.response import ResponseModel
from app.core.shared.application.utils import success_response
from app.core.shared.infrastructure.database.database import get_db
from app.core.shared.security.jwt import JWTService
from app.core.shared.security.password_hasher import PasswordHasher
from app.core.user.api.schemas.user_schemas import CreateUserResponseSchema, CreateUserSchema, LoginUserResponseSchema, LoginUserSchema
from app.core.user.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from app.core.user.application.use_cases.login_user_use_case import LoginUserUseCase
from app.core.user.domain.commands.create_user_command import CreateUserCommand
from app.core.user.domain.commands.login_user_command import LoginUserCommand
from app.core.user.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)

router = APIRouter()


@router.post(
    "/auth/register",
    response_model=ResponseModel[CreateUserResponseSchema],
    status_code=status.HTTP_201_CREATED
)
def create_user(input: CreateUserSchema, db: Session = Depends(get_db)):
    password_hasher = PasswordHasher()
    user_repository = SqlAlchemyUserRepository(db)
    use_case = CreateUserUseCase(user_repository, password_hasher)
    command = CreateUserCommand(
        username=input.username, email=input.email, password=input.password)
    try:
        event = use_case.execute(command)
        return success_response(event, "User created successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/auth/login', response_model=ResponseModel[LoginUserResponseSchema])
def login_user(input: LoginUserSchema, db: Session = Depends(get_db)):
    password_hasher = PasswordHasher()
    user_repository = SqlAlchemyUserRepository(db)
    jwt_service = JWTService()
    use_case = LoginUserUseCase(user_repository, password_hasher, jwt_service)
    command = LoginUserCommand(email=input.email, password=input.password)
    try:
        event = use_case.execute(command)
        return success_response(event, "User logged in successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
