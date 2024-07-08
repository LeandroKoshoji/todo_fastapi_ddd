from sqlalchemy import Column, DateTime, String, func

from app.core.shared.infrastructure.database.database import Base
from app.core.shared.infrastructure.database.guid import GUID


class User(Base):
    __tablename__ = 'users'

    id = Column(GUID(), primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
