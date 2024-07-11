from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.orm import relationship

from app.core.shared.infra.database.database import Base
from app.core.task.domain.task import TaskStatus


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus),
                    default=TaskStatus.PENDING, nullable=False)
    user_id = Column(
        SQLAlchemyUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )
    send_notification = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="tasks")
