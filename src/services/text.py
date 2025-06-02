from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal

from loguru import logger

from src.db.repository import PromptRepository
from src.services.exceptions import ErrorMessages, MaxCounterError
from src.services.gpt import GPTRequests

if TYPE_CHECKING:
    from src.db.manager import AsyncPGManager
    from src.models.news import FormattingData, NewsData


class TextAdapter:

    max_tries = 5

    def __init__(self, gpt: GPTRequests, max_length: int):
        self.gpt = gpt
        self.max_length = max_length

    async def adapt(self, prompt: str, original_text: str) -> str:
        counter = 0
        while True:
            adapted_text = await self.gpt.adapt_text(prompt, original_text)

            if (
                len(adapted_text) > self.max_length
                or len(adapted_text) < self.max_length / 2
            ):
                if counter >= self.max_tries:
                    raise MaxCounterError(ErrorMessages.MAX_TRIES.value)

                logger.info(
                    f"Попытка {counter + 1}: Длина вне диапазона ({len(adapted_text)}). Повтор.",
                )
                counter += 1
            else:
                logger.info(f"Текст успешно адаптирован, длина: {len(adapted_text)}.")
                return adapted_text


class TextFormatter(ABC):

    def __init__(
        self,
        news: NewsData,
        configs: FormattingData,
        db_manager: AsyncPGManager,
    ):
        self.news = news
        self.configs = configs
        self.gpt = GPTRequests(language=self.configs.language)
        self.prompt_repository = PromptRepository(db_manager)

    @property
    @abstractmethod
    def max_length(self) -> int:
        pass

    @abstractmethod
    async def format(self):
        pass

    def _get_adapter(self):
        return TextAdapter(self.gpt, self.max_length)

    @abstractmethod
    async def get_prompt(self) -> str:
        pass

    @property
    def format_type(self) -> Literal["summarized", "article", "newsfeed", "video"]:
        return self.configs.format_type

    @property
    def title(self) -> str:
        return self.news.title

    @property
    def language(self) -> str:
        return self.configs.language

    @property
    def extra_msg(self):
        return self.configs.extra_text_after_formatting

    @property
    def extra_prompt(self):
        return self.configs.extra_prompt
