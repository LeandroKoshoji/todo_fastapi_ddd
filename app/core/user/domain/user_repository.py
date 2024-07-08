from abc import ABC, abstractmethod

from app.core.user.domain.user import User, UserId


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: UserId) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def save_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, user_id: UserId) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        raise NotImplementedError
