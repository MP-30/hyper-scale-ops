from http import HTTPStatus

from app.exceptions.base import AppException


class StudentNotFoundException(AppException):
    def __init__(self, student_id: int):
        super().__init__(
            message=f"Student with id '{student_id}' not found.",
            status_code=HTTPStatus.NOT_FOUND,
            error_code="STUDENT_NOT_FOUND",
        )


class StudentAlreadyExistsException(AppException):
    def __init__(self, roll_number: str):
        super().__init__(
            message=f"Student with roll number '{roll_number}' already exists.",
            status_code=HTTPStatus.CONFLICT,
            error_code="STUDENT_ALREADY_EXISTS",
        )