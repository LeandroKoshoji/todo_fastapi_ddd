from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    status: str
    message: str
    data: Optional[T] = None


class PaginatedResponseModel(BaseModel, Generic[T]):
    status: str
    message: str
    data: list[T]
    page: int
    per_page: int
    total: int
