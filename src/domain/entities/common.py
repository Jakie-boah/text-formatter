from __future__ import annotations

from typing import Literal
from src.domain.models.feed import FeedSeo
from pydantic import BaseModel


class NewsData(BaseModel):
    title: str
    published_date: str
    url: str
    publisher: str
    description: str
    text: str
    img: str | None = ""
    summary: str | None = ""


class Connection(BaseModel):
    connection_id: str | int
    connection_name: str
    is_connection_primary: bool
    account_id: str
    access_token: str


class TaskExecutionData(BaseModel):
    user_id: int
    feed: dict
    connection: Connection
    news: NewsData
    formatting_result: dict
    feed_type: Literal["newsfeed", "video", "article"]

    @property
    def feed_id(self):
        return self.feed.get("feed_id")

    @property
    def feed_title(self):
        return self.feed.get("feed_title")

    @property
    def feed_seo(self):
        return FeedSeo(
            seo_boost=self.feed.get("seo_boost"),
            show_news_source=self.feed.get("show_news_source"),
        )
