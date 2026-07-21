from http import HTTPStatus

from app.exceptions.base import AppException


class TeacherNotFoundException(AppException):
    def __init__(self, teacher_id: int):
        super().__init__(
            message=f"Teacher with id '{teacher_id}' not found",
            status_code=HTTPStatus.NOT_FOUND,
            error_code="TEACHER_NOT_FOUND",
        )