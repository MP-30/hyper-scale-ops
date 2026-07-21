from http import HTTPStatus

from app.exceptions.base import AppException


class DatabaseException(AppException):
    def __init__(self, message: str = "Database operation failed."):
        super().__init__(
            message=message,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            error_code="DATABASE_ERROR",
        )