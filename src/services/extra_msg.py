from typing import TypeAlias
from src.services.feed_backend import FeedBackend
from loguru import logger
from src.models.feed import ExtraMsgData

ExtraMsg: TypeAlias = str


class BaseExtraMsg:
    def __init__(self, data: ExtraMsgData):
        self.news = data.news
        self.feed_record = data.feed_record

        if self.feed_record.seo_boost:
            self.seo_boost_static_url = data.feed_record.seo_boost.static_url
            self.seo_boost_text = data.feed_record.seo_boost.text
        else:
            self.seo_boost_static_url = ""
            self.seo_boost_text = ""


class ExtraMsgMainConnection(BaseExtraMsg):

    def build_msg(self) -> ExtraMsg:
        parts = [self.seo_boost_text]

        if self.feed_record.show_news_source:
            parts.append(self.news.url)

        elif self.seo_boost_static_url:
            parts.append(self.seo_boost_static_url)
        else:
            pass

        logger.info("extra msg:")
        logger.info([part for part in parts if part])

        return "\n" + "\n".join(part for part in parts if part) + "\n" if parts else ""


class ExtraMsgSecondaryConnection(BaseExtraMsg):

    def build_msg(self) -> ExtraMsg:
        parts = [self.seo_boost_text]
        if self.seo_boost_static_url:
            parts.append(self.seo_boost_static_url)
        else:
            parts.append(self.feed_record.url_for_primary_connection)

        logger.info("extra msg:")
        logger.info([part for part in parts if part])

        return "\n" + "\n".join(part for part in parts if part) + "\n" if parts else ""


class ExtraMsgService:
    def __init__(self, feed_id, main_connection, news):
        self.feed_id = feed_id
        self.main_connection = main_connection
        self.news = news

    async def build_msg(self) -> ExtraMsg:
        feed = await FeedBackend.get_formatting_data_for_feed(feed_id=self.feed_id)
        data = ExtraMsgData(feed_record=feed, news=self.news)
        if self.main_connection:
            return ExtraMsgMainConnection(data).build_msg()
        else:
            return ExtraMsgSecondaryConnection(data).build_msg()
