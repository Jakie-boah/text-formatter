from __future__ import annotations

from pydantic import BaseModel, field_validator


class SeoBoost(BaseModel):
    text: str | None = None
    static_url: str | None = None


class FeedSeo(BaseModel):
    seo_boost: SeoBoost | None = None
    show_news_source: bool
    url_for_primary_connection: str | None = ""


class FeedPrompt(BaseModel):
    text_prompt: str | None = ""
    refining_prompt: str | None = ""

    @field_validator("text_prompt", "refining_prompt")
    def ensure_newlines_if_not_empty(cls, v):  # noqa: N805
        if not v:
            v = ""
        return v

    @property
    def prompt(self):
        return f"{self.text_prompt} {self.refining_prompt}"


class ExtraMsgData(BaseModel):
    feed_record: FeedSeo
    news_source: str | None = ""
