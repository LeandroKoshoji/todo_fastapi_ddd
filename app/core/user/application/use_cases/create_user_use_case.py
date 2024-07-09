from app.core.shared.security.interfaces import PasswordHasherInterface
from app.core.user.domain.commands.create_user_command import CreateUserCommand
from app.core.user.domain.events.user_created_event import UserCreatedEvent
from app.core.user.domain.user import User
from app.core.user.domain.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hash_service: PasswordHasherInterface
    ):
        self.user_repository = user_repository
        self.password_hash_service = password_hash_service

    def execute(self, command: CreateUserCommand) -> UserCreatedEvent:
        user = User(
            username=command.username,
            email=command.email,
            hashed_password=(
                self.password_hash_service.hash_password(command.password)
            ),
        )

        user_email_exists = self.user_repository.get_user_by_email(user.email)

        if user_email_exists:
            raise ValueError('User already exists')

        self.user_repository.save_user(user)

        user_data = user.to_dict()
        return UserCreatedEvent(
            id=user_data['id'],
            username=user_data['username'],
            email=user_data['email'],
            created_at=user_data['created_at']
        )
