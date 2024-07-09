from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class CreateUserResponseSchema(BaseModel):
    id: str
    username: str
    email: str
    created_at: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class LoginUserResponseSchema(BaseModel):
    token: str
    token_type: str
    expires_in: str
