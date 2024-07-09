from app.core.shared.security.interfaces import JWTInterface, PasswordHasherInterface
from app.core.user.domain.commands.login_user_command import LoginUserCommand
from app.core.user.domain.events.user_loggedin_event import UserLoggedInEvent
from app.core.user.domain.user_repository import UserRepository


class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, hash_service: PasswordHasherInterface, jwt_service: JWTInterface):
        self.user_repository = user_repository
        self.hash_service = hash_service
        self.jwt_service = jwt_service

    def execute(self, command: LoginUserCommand) -> UserLoggedInEvent:
        user = self.user_repository.get_user_by_email(command.email)

        if not user:
            raise ValueError('Invalid credentials')

        if not self.hash_service.verify_password(command.password, user.hashed_password):
            raise ValueError('Invalid credentials')

        token = self.jwt_service.create_access_token(data={'sub': user.email})

        return UserLoggedInEvent(
            token=token['token'],
            token_type=token['token_type'],
            expires_in=token['expires_in']
        )
