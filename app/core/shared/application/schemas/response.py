from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')


class ResponseModel(GenericModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None
