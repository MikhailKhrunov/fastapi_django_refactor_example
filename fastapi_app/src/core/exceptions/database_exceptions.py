"""Инфраструктурные исключения (работа с БД)"""


class DatabaseError(Exception):
    """Базовое исключение для ошибок БД"""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class RecordNotFoundError(DatabaseError):
    """Запись не найдена"""

    def __init__(
        self,
        entity: str,
        entity_id: int,
        original_error: Exception = None
    ):
        self.entity = entity
        self.entity_id = entity_id
        message = f"{entity} с ID {entity_id} не найден"
        super().__init__(message, original_error)


class ForeignKeyError(DatabaseError):
    """Ошибка внешнего ключа"""

    def __init__(
        self,
        field: str,
        referenced: str,
        value: int,
        original_error: Exception = None
    ):
        self.field = field
        self.referenced = referenced
        self.value = value
        message = f"Не найдена запись {referenced} с ID {value} для поля {field}"
        super().__init__(message, original_error)


class DatabaseOperationError(DatabaseError):
    """Ошибка операции в БД"""

    pass
