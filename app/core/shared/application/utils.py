from typing import Any

from app.core.shared.application.schemas.response import PaginatedResponseModel, ResponseModel


def success_response(data: Any, message: str = "Success"):
    return ResponseModel(
        status="success",
        message=message,
        data=data
    )


def paginated_response(data: Any,  message: str, page: int, per_page: int, total: int):
    return PaginatedResponseModel(
        status="success",
        message=message,
        data=data,
        page=page,
        per_page=per_page,
        total=total
    )
