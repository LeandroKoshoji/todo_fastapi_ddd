from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.core.shared.security.jwt import JWTService
from app.core.user.infrastructure.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.core.shared.infrastructure.database.database import get_db
from app.config.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    jwt_service = JWTService()
    try:
        payload = jwt_service.verify_access_token(token)
        if payload is None:
            raise credentials_exception
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = SqlAlchemyUserRepository(db).get_user_by_id(user_id=user_id)
    print('user', user)
    if user is None:
        raise credentials_exception
    return {"id": user.id, "username": user.username, "email": user.email}
