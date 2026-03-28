"""API исключения (HTTP ошибки)"""

from fastapi import HTTPException, status


class APIException(HTTPException):
    """Базовое исключение для API"""
    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: str = None,
        details: dict = None
    ):
        self.error_code = error_code or "API_ERROR"
        self.details = details or {}
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "error_code": self.error_code,
                "details": self.details
            }
        )


class NotFoundException(APIException):
    """404 - Не найдено"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message,
            status.HTTP_404_NOT_FOUND,
            "NOT_FOUND",
            details
        )


class BadRequestException(APIException):
    """400 - Неправильный запрос"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message,
            status.HTTP_400_BAD_REQUEST,
            "BAD_REQUEST",
            details
        )


class InternalServerException(APIException):
    """500 - Внутренняя ошибка"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            message,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "INTERNAL_ERROR",
            details
        )
