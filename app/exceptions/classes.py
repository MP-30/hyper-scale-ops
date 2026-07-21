from http import HTTPStatus

from app.exceptions.base import AppException


class ClassNotFoundException(AppException):
    def __init__(self, class_id: int):
        super().__init__(
            message=f"Class with id '{class_id}' not found.",
            status_code=HTTPStatus.NOT_FOUND,
            error_code="CLASS_NOT_FOUND",
        )