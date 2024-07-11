from dataclasses import dataclass


@dataclass
class TaskEditedEvent:
    id: str
    user_id: str
    title: str
    status: str
    description: str
    send_notification: bool
    created_at: str
    updated_at: str
