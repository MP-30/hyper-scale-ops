from http import HTTPStatus

from app.exceptions.base import AppException


class PeriodNotFoundException(AppException):
    def __init__(self, period_id: int):
        super().__init__(
            message=f"Period with id '{period_id}' not found",
            status_code=HTTPStatus.NOT_FOUND,
            error_code="PERIOD_NOT_FOUND",
        )