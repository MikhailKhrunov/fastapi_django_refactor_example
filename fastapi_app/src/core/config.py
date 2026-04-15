from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Приложение
    APP_TITLE: str = "fastapi kittygram"
    APP_VERSION: str = "1.0.0"

    # Сервер
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = False

    # База данных
    DATABASE_URL: str = "sqlite:///./kittygram.db"

    # JWT
    SECRET_KEY: str = "jkbdqhvwekdkwjbwhjebdgwbbqwxs818247nanskxmq"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Логирование
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
