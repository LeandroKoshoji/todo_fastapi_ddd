from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config.settings import Settings
from app.core.shared.security.interfaces import JWTInterface


class JWTService(JWTInterface):
    def __init__(self):
        self.secret_key = Settings().SECRET_KEY
        self.algorithm = 'HS256'
        self.access_token_expire_minutes = 30

    def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(
                timezone.utc) + timedelta(
                    minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm)
        return {'token': encoded_jwt, 'token_type': 'bearer', 'expires_in': expire.isoformat()}

    def verify_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key,
                                 algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
