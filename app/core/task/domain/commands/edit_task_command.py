import uuid
from dataclasses import dataclass


@dataclass
class EditTaskCommand:
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    status: str
    description: str
    send_notification: bool
