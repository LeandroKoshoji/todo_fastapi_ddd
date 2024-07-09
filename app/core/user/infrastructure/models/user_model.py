from sqlalchemy import Column, DateTime, String, func

from app.core.shared.infrastructure.database.database import Base
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID


class User(Base):
    __tablename__ = 'users'

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
