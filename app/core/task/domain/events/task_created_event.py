from dataclasses import dataclass


@dataclass
class TaskCreatedEvent:
    id: str
    title: str
    user_id: str
    status: str
    description: str
    send_notification: bool
    created_at: str
    updated_at: str
