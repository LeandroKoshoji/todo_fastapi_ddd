import uuid
from dataclasses import dataclass


@dataclass
class DeleteTaskCommand:
    id: uuid.UUID
