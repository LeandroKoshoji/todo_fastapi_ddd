from dataclasses import dataclass


@dataclass
class UserCreatedEvent:
    id: str
    username: str
    email: str
    created_at: str
