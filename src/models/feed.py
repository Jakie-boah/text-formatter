from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from src.models.news import NewsData

if TYPE_CHECKING:
    from src.models.news import NewsData


class SeoBoost(BaseModel):
    text: str | None = None
    static_url: str | None = None


class NewsFeed(BaseModel):
    seo_boost: SeoBoost | None = None
    show_news_source: bool
    url_for_primary_connection: str | None = ""


class ExtraMsgData(BaseModel):
    feed_record: NewsFeed
    news: NewsData
