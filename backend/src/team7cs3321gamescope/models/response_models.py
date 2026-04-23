from typing import Any, Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str


class ApiResponse(BaseModel):
    status: str
    data: Optional[Any] = None
    error: Optional[ErrorDetail] = None
