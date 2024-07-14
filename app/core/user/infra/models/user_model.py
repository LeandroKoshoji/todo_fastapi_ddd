from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.orm import relationship

from app.core.shared.infra.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    tasks = relationship("Task", back_populates="user",
                         cascade="all, delete-orphan")