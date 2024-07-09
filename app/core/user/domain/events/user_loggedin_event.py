from dataclasses import dataclass


@dataclass
class UserLoggedInEvent:
    token: str
    token_type: str
    expires_in: str
