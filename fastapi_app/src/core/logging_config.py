import logging
import sys
from core.config import settings


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format=LOG_FORMAT,
    handlers=[logging.StreamHandler(sys.stdout)]
)

user_logger = logging.getLogger("user_actions")


def log_user_action(user_id: int, action: str, details: dict = None):
    user_logger.info(
        f"User {user_id}: {action}",
        extra={"user_id": user_id, "action": action, "details": details or {}}
    )
