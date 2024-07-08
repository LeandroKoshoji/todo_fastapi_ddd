import uuid
from abc import ABC
from dataclasses import dataclass, field


@dataclass
class Entity(ABC):
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __eq__(self, other: "Entity") -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
