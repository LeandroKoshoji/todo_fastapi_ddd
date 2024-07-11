from dataclasses import dataclass
import uuid


@dataclass
class EditTaskCommand:
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    status: str
    description: str
    send_notification: bool
