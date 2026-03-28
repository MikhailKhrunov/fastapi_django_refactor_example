"""Доменные исключения (бизнес-логика)"""


class DomainError(Exception):
    """Базовое доменное исключение"""
    def __init__(
        self,
        message: str,
        error_code: str = None,
        details: dict = None
    ):
        self.message = message
        self.error_code = error_code or "DOMAIN_ERROR"
        self.details = details or {}
        super().__init__(self.message)


class EntityNotFoundError(DomainError):
    """Сущность не найдена"""
    def __init__(self, entity: str, entity_id: int, details: dict = None):
        self.entity = entity
        self.entity_id = entity_id
        message = f"{entity} с ID {entity_id} не найден"
        super().__init__(message, f"{entity.upper()}_NOT_FOUND", details)


class OwnerNotFoundError(DomainError):
    """Владелец не найден"""
    def __init__(self, owner_id: int, details: dict = None):
        self.owner_id = owner_id
        message = f"Владелец с ID {owner_id} не найден"
        super().__init__(message, "OWNER_NOT_FOUND", details)
