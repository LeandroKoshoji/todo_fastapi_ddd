from dataclasses import dataclass
import uuid


@dataclass
class DeleteTaskCommand:
    id: uuid.UUID
