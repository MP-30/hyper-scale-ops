import sys
from pathlib import Path

from loguru import logger

from app.core.request_context import get_request_id

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.configure(
    extra={
        "request_id": "-"
    }
)

logger.add(
    sys.stdout,
    level="INFO",
    serialize=False,
    enqueue=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "{extra[request_id]} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)

logger.add(
    LOG_DIR / "application.log",
    level="INFO",
    rotation="20 MB",
    retention="15 days",
    compression="zip",
    serialize=True,
    enqueue=True,
)

app_logger = logger.patch(
    lambda record: record["extra"].update(
        request_id=get_request_id()
    )
)