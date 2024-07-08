import uuid

from sqlalchemy.dialects.postgresql import UUID as PostgreSQL_UUID
from sqlalchemy.types import CHAR, TypeDecorator


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses PostgreSQL's UUID type, otherwise uses CHAR(32), storing as 
    stringified hex values.
    """
    impl = CHAR

    @staticmethod
    def load_dialect_impl(dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PostgreSQL_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(32))

    @staticmethod
    def process_bind_param(value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        elif not isinstance(value, uuid.UUID):
            return "%.32x" % uuid.UUID(value).int
        else:
            return "%.32x" % value.int

    @staticmethod
    def process_result_value(value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)
