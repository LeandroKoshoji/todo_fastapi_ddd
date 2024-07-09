from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
