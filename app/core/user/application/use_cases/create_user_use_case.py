from app.core.user.domain.commands.create_user_command import CreateUserCommand
from app.core.user.domain.events.user_created_event import UserCreatedEvent
from app.core.user.domain.user import User
from app.core.user.domain.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, command: CreateUserCommand) -> UserCreatedEvent:
        user = User(
            username=command.username,
            email=command.email,
            hashed_password=command.password,
            # todo: adicionar service de hash de senha
        )

        self.user_repository.save_user(user)

        return UserCreatedEvent(id=user.id, username=user.username, email=user.email, created_at=user.created_at)
