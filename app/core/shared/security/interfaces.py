from abc import ABC, abstractmethod
from datetime import timedelta


class PasswordHasherInterface(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(
        self,
        plain_password: str,
        hashed_password: str
    ) -> bool:
        pass


class JWTInterface(ABC):
    @abstractmethod
    def create_access_token(
            self,
            data: dict,
            expires_delta: timedelta = None
    ) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> dict:
        pass
