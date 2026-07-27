from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.logger import app_logger
from app.exceptions.base import AppException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        app_logger.bind(
            event="app_exception",
            path=request.url.path,
            method=request.method,
            status_code=exc.status_code,
            error_code=exc.error_code,
            exception_type=type(exc).__name__,
        ).warning(exc.message)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "detail": exc.message.rstrip("."),
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                },
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        app_logger.bind(
            event="validation_error",
            path=request.url.path,
            method=request.method,
            status_code=422,
            exception_type=type(exc).__name__,
            errors=exc.errors(),
        ).warning("Request validation failed")

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "detail": exc.errors(),
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation Failed",
                    "details": exc.errors(),
                },
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_handler(request: Request, exc: IntegrityError):
        app_logger.bind(
            event="database_constraint",
            path=request.url.path,
            method=request.method,
            status_code=409,
            exception_type=type(exc).__name__,
        ).exception("Database constraint violation")

        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "detail": "Database constraint violation.",
                "error": {
                    "code": "DATABASE_CONSTRAINT",
                    "message": "Database constraint violation.",
                },
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_handler(request: Request, exc: SQLAlchemyError):
        app_logger.bind(
            event="database_error",
            path=request.url.path,
            method=request.method,
            status_code=500,
            exception_type=type(exc).__name__,
        ).exception("Database error")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "detail": "Database error.",
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "Database error.",
                },
            },
        )

    @app.exception_handler(Exception)
    async def global_handler(request: Request, exc: Exception):
        app_logger.bind(
            event="unhandled_exception",
            path=request.url.path,
            method=request.method,
            status_code=500,
            exception_type=type(exc).__name__,
        ).exception("Unhandled exception")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "detail": "Unexpected error occurred.",
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Unexpected error occurred.",
                },
            },
        )