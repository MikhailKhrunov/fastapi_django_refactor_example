import asyncio
import uvicorn
import logging
from pathlib import Path

from app import create_app
from database import Base, engine
from core.config import settings
from core.logging_config import log_user_action

logger = logging.getLogger(__name__)


def run_migrations():
    """Запустить миграции Alembic при старте"""
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config(Path("./alembic.ini"))
    print(alembic_cfg.__str__)
    logger.info(msg=alembic_cfg)
    alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    command.upgrade(alembic_cfg, "head")
    logger.info("Migrations done")


async def run() -> None:
    # Запуск миграций
    run_migrations()

    # Логирование старта
    log_user_action(
        0,
        "SERVER_START",
        {"host": settings.HOST, "port": settings.PORT}
    )
    app = create_app()

    config = uvicorn.Config(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
    server = uvicorn.Server(config=config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run())
