from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from pytest import Session

from app.core.shared.infrastructure.database.database import Base, engine, get_db
from app.core.user.domain.commands.create_user_command import CreateUserCommand
from app.core.user.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.core.user.application.use_cases.create_user_use_case import CreateUserUseCase

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Hello World!'}


class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserSchema(BaseModel):
    id: str
    username: str
    email: str
    created_at: str


@app.post("/users")
def create_user(input: CreateUserSchema, db: Session = Depends(get_db)):
    user_repository = SqlAlchemyUserRepository(db)
    use_case = CreateUserUseCase(user_repository)
    command = CreateUserCommand(
        username=input.username, email=input.email, password=input.password)
    try:
        event = use_case.execute(command)
        return {"event": event}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
