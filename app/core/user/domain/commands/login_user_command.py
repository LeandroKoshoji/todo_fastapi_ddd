from dataclasses import dataclass


@dataclass
class LoginUserCommand:
    email: str
    password: str
