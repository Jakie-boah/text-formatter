import sys
from pathlib import Path

from loguru import logger


def setup_logging():
    logger.remove()

    logger.add(
        "/usr/src/app/logs/formatting/log_on_{time:YYYY-MM-DD}.log",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        encoding="utf-8",
        level="DEBUG",
        filter=lambda record: not is_celery_log(record),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    )
    logger.add(
        "/usr/src/app/logs/celery/log_on_{time:YYYY-MM-DD}.log",
        rotation="10 MB",
        filter=is_celery_log,
        format="{time:YYYY-MM-DD HH:mm:ss} | CELERY | {message}",
        level="DEBUG",
    )
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}"
               "</level> | {name}:{function}:{line} | <cyan>{message}</cyan>",
        level="INFO",
        colorize=True,
    )


def is_celery_log(record):
    """Проверяет, относится ли лог к celery"""
    try:
        path = str(Path(record["file"].path).resolve())
    except (AttributeError, TypeError):
        return False

    else:
        return "celery" in path
