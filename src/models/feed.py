from __future__ import annotations

from pydantic import BaseModel


class SeoBoost(BaseModel):
    text: str | None = None
    static_url: str | None = None


class NewsFeed(BaseModel):
    seo_boost: SeoBoost | None = None
    show_news_source: bool
    url_for_primary_connection: str | None = ""


class ExtraMsgData(BaseModel):
    feed_record: NewsFeed
    news_source: str | None = ""
