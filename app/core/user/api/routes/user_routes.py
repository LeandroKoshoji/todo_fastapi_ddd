from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.shared.application.schemas.response import ResponseModel
from app.core.shared.application.utils import success_response
from app.core.shared.infra.database.database import get_db
from app.core.shared.security.dependecies import get_current_user
from app.core.shared.security.jwt import JWTService
from app.core.shared.security.password_hasher import PasswordHasher
from app.core.user.api.schemas.user_schemas import (
    CreateUserResponseSchema,
    CreateUserSchema,
    LoginUserResponseSchema,
    LoginUserSchema,
)
from app.core.user.application.factories.use_case_factory import (
    create_create_user_use_case,
    create_login_user_use_case,
)
from app.core.user.domain.commands.create_user_command import CreateUserCommand
from app.core.user.domain.commands.login_user_command import LoginUserCommand
from app.core.user.domain.exceptions import InvalidCredentialsError
from app.core.user.infra.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)

router = APIRouter()
# todo: criar um arquivo para ser o handler dos erros de usuario


@router.post(
    "/auth/register",
    response_model=ResponseModel[CreateUserResponseSchema],
    status_code=status.HTTP_201_CREATED
)
def create_user(input: CreateUserSchema, db: Session = Depends(get_db)):
    use_case = create_create_user_use_case(db)
    command = CreateUserCommand(
        username=input.username, email=input.email, password=input.password)
    try:
        event = use_case.execute(command)
        return success_response(event, "User created successfully")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    '/auth/login',
    response_model=ResponseModel[LoginUserResponseSchema]
)
def login_user(input: LoginUserSchema, db: Session = Depends(get_db)):
    use_case = create_login_user_use_case(db)
    command = LoginUserCommand(email=input.email, password=input.password)
    try:
        event = use_case.execute(command)
        return success_response(event, "User logged in successfully")

    except InvalidCredentialsError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/auth/token')
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    This route is used to generate an access token at /docs
    """
    user_repo = SqlAlchemyUserRepository(db)
    user = user_repo.get_user_by_email(form_data.username)
    if user is None or not PasswordHasher().verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    jwt_service = JWTService()
    access_token = jwt_service.create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token['token'],
        "token_type": access_token['token_type'],
        "expires_in": access_token['expires_in']
    }


@router.get('/auth/me')
def get_me(current_user=Depends(get_current_user)):
    """
    This route is just to test authentication guard at /docs
    """
    return current_user
