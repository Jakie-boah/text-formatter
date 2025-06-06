from __future__ import annotations

from enum import Enum, auto

from loguru import logger


class ErrorMessages(Enum):
    MAX_TRIES = "Превышено кол-во запросов к нейронке - не получилось войти в лимит по кол-ву символов"
    POOL_ERROR = "Pool is not initialized. Call connect() first."
    ABS_METHOD_NOT_IMPLEMENTED = "Subclasses must implement build_msg()"

    def format(self, *args) -> str:
        return self.value % args


class ObjTypes(Enum):
    NewsFeed = auto()
    CustomPrompts = auto()
    FeedArticles = auto()


class MaxCounterError(Exception):
    def __init__(self, message: str, *, original_exception: Exception | None = None):
        self.message = message
        self.original_exception = original_exception

        logger.error(f"{self.__class__.__name__}: {message}")
        if original_exception:
            logger.exception(original_exception)

        super().__init__(message)
