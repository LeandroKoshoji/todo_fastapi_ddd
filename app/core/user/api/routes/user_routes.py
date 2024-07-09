from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.shared.application.schemas.response import ResponseModel
from app.core.shared.application.utils import success_response
from app.core.shared.infrastructure.database.database import get_db
from app.core.user.api.schemas.user_schemas import CreateUserSchema
from app.core.user.application.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from app.core.user.domain.commands.create_user_command import CreateUserCommand
from app.core.user.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)

router = APIRouter()


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    created_at: str


@router.post(
    "/",
    response_model=ResponseModel[UserOut],
    status_code=status.HTTP_201_CREATED
)
def create_user(input: CreateUserSchema, db: Session = Depends(get_db)):
    user_repository = SqlAlchemyUserRepository(db)
    use_case = CreateUserUseCase(user_repository)
    command = CreateUserCommand(
        username=input.username, email=input.email, password=input.password)
    try:
        event = use_case.execute(command)
        return success_response(event, "User created successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
