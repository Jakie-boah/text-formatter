from __future__ import annotations

from abc import ABC, abstractmethod
from pydantic import BaseModel, field_validator
from typing import Literal, Optional
from src.services.gpt import GPTRequests


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
    extra_prompt: str | None = ""
    extra_text_after_formatting: str | None = ""

    @field_validator("extra_prompt", "extra_text_after_formatting")
    def ensure_newlines_if_not_empty(cls, v):
        if v and not v.startswith("\n"):
            v = f"\n{v}"
        if v and not v.endswith("\n"):
            v = f"{v}\n"
        return v


class TextFormatter(ABC):
    def __init__(
        self,
        news: NewsData,
        configs: FormattingData,
    ):
        self.news = news
        self.configs = configs
        self.gpt = GPTRequests(language=self.configs.language)

    @abstractmethod
    async def format(self):
        pass

    @abstractmethod
    async def get_prompt(self) -> str:
        pass

    @property
    def format_type(self) -> Literal["default", "summarized"]:
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
