import uuid
from dataclasses import dataclass
from typing import Optional

from app.core.task.domain.task import TaskStatus


@dataclass
class CreateTaskCommand:
    title: str
    user_id: uuid.UUID
    status: TaskStatus
    description: Optional[str] = None
    send_notification: Optional[bool] = False
