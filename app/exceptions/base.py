from http import HTTPStatus


class AppException(Exception):
    """
    Base exception for all of my application-specific exceptions.
    """

    def __init__(
        self,
        message: str,
        status_code: int = HTTPStatus.BAD_REQUEST,
        error_code: str = "APP_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)