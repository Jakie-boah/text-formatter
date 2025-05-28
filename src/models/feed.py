from __future__ import annotations


from pydantic import BaseModel


class SeoBoost(BaseModel):
    link_to_full_news: bool
    text: str | None = None
    static_url: str | None = None
    prefix: str | None = None


class NewsFeed(BaseModel):
    primary_logic: bool
    feed_connections_length: int
    seo_boost: SeoBoost | None = None
    show_news_source: bool
    url_for_primary_connection: str | None = ""
