import datetime
import uuid
from dataclasses import dataclass, field

from app.core.shared.domain.entity import Entity


class UserId:
    id: uuid.UUID


@dataclass
class User(Entity):
    username: str
    email: str
    hashed_password: str
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc), init=False)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.username:
            raise ValueError("Username is required")
        if len(self.username) > 255:
            raise ValueError("Username must be less than 255 characters")
        if len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not self.email:
            raise ValueError("Email is required")

    def change_password(self, new_password: str):
        self.hashed_password = new_password

    def change_username(self, new_username: str):
        self.username = new_username
        self.validate()

    def change_email(self, new_email: str):
        self.email = new_email
        self.validate()

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "created_at": self.created_at
        }
