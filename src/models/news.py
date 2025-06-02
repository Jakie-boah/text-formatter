from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, field_validator


class NewsData(BaseModel):
    title: str
    published_date: str
    url: str
    publisher: str
    description: str
    text: str
    img: str | None = ""
    summary: str | None = ""


class FormattingData(BaseModel):
    language: str
    format_type: Literal["summarized", "article", "newsfeed", "video"] = "newsfeed"
    extra_prompt: str | None = ""
    extra_text_after_formatting: str | None = ""

    @field_validator("extra_prompt", "extra_text_after_formatting")
    def ensure_newlines_if_not_empty(cls, v):  # noqa: N805
        if v and not v.startswith("\n"):
            v = f"\n{v}"
        if v and not v.endswith("\n"):
            v = f"{v}\n"
        return v
