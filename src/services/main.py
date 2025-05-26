from __future__ import annotations

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Literal, Optional


class NewsData(BaseModel):
    title: str
    published_date: str
    url: str
    publisher: str
    description: str
    text: str
    img: str | None = None
    summary: Optional[str] = None


class FormattingData(BaseModel):
    language: str
    format_type: Literal["default", "summarized"] = "default"
    extra_prompt: str | None = None
    extra_text_after_formatting: str | None = None


class TextFormatter(ABC):
    def __init__(
        self,
        news: NewsData,
        configs: FormattingData,
    ):
        self.news = news
        self.configs = configs

    @abstractmethod
    async def format(self):
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        pass
