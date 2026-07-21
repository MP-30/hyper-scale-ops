from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: T | None = None


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail