from typing import Any

from app.core.shared.application.schemas.response import ResponseModel


def success_response(data: Any, message: str = "Success"):
    return ResponseModel(
        status="success",
        message=message,
        data=data
    )
