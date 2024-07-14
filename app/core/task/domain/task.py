import datetime
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from app.core.shared.domain.entity import Entity
from app.core.task.domain.exceptions import InvalidDomainRuleError

MAX_TITLE_LENGTH = 255
MAX_DESCRIPTION_LENGTH = 255


@dataclass
class TaskId:
    id: uuid.UUID = field(default_factory=uuid.uuid4)


class TaskStatus(str, Enum):
    PENDING = 'pending'
    ON_GOING = 'on_going'
    DONE = 'done'


@dataclass
class Task(Entity):
    title: str
    user_id: uuid.UUID
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    send_notification: bool = False
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    def __post_init__(self):
        self.validate()

    def validate(self):
        if not self.title:
            raise InvalidDomainRuleError('Title is required')
        if len(self.title) > MAX_TITLE_LENGTH:
            raise InvalidDomainRuleError(
                'Title must be less than 255 characters')
        if self.description and len(self.description) > MAX_DESCRIPTION_LENGTH:
            raise InvalidDomainRuleError(
                'Description must be less than 255 characters')
        if not self.user_id:
            raise InvalidDomainRuleError('User id is required')
        try:
            TaskStatus(self.status)
        except ValueError:
            raise InvalidDomainRuleError('Invalid status')

    def change_title(self, new_title: str):
        self.title = new_title
        self.validate()

    def change_description(self, new_description: str):
        self.description = new_description
        self.validate()

    def change_status(self, new_status: TaskStatus):
        self.status = new_status
        self.validate()

    def change_send_notification(self, new_send_notification: bool):
        self.send_notification = new_send_notification
        self.validate()

    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'user_id': str(self.user_id),
            'description': self.description,
            'status': self.status,
            'send_notification': self.send_notification,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
