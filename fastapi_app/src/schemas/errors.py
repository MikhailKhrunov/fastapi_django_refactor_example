"""Схемы ошибок для Swagger UI"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class ErrorDetail(BaseModel):
    """Детали ошибки"""
    message: str = Field(
        ...,
        description="Сообщение об ошибке"
    )
    error_code: str = Field(
        ...,
        description="Код ошибки"
    )
    details: Dict[str, Any] = Field(
        default_factory=dict,
        description="Информация"
    )


class ErrorResponse(BaseModel):
    """Стандартный ответ с ошибкой"""
    detail: ErrorDetail


class ValidationErrorDetail(BaseModel):
    """Деталь ошибки валидации"""
    loc: list = Field(..., description="Путь к полю с ошибкой")
    msg: str = Field(..., description="Сообщение об ошибке")
    type: str = Field(..., description="Тип ошибки")


class ValidationErrorResponse(BaseModel):
    """Ответ с ошибкой валидации (422)"""
    detail: list[ValidationErrorDetail]
