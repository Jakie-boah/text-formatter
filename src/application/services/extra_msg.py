from abc import ABC, abstractmethod
from typing import TypeAlias
from src.domain.models.feed import FeedSeo
from loguru import logger

from src.domain.models.feed import ExtraMsgData
from src.application.services.exceptions import ErrorMessages

ExtraMsg: TypeAlias = str


class BaseExtraMsg(ABC):
    def __init__(self, data: ExtraMsgData):
        self._data = data

    @property
    def seo_boost_static_url(self) -> str:
        seo_boost = self._data.feed_record.seo_boost
        return seo_boost.static_url if seo_boost else ""

    @property
    def seo_boost_text(self) -> str:
        seo_boost = self._data.feed_record.seo_boost
        return seo_boost.text if seo_boost else ""

    @property
    def news_source(self) -> str:
        return self._data.news_source

    @property
    def feed_record(self):
        return self._data.feed_record

    @abstractmethod
    def build_msg(self) -> ExtraMsg:
        raise NotImplementedError(ErrorMessages.ABS_METHOD_NOT_IMPLEMENTED.value)

    @staticmethod
    def _format(parts: list[str]) -> ExtraMsg:
        filtered_parts = [part for part in parts if part]
        logger.info("extra msg:")
        logger.info(filtered_parts)
        return "\n" + "\n".join(filtered_parts) + "\n" if filtered_parts else ""


class ExtraMsgMainConnection(BaseExtraMsg):
    def build_msg(self) -> ExtraMsg:
        parts = [self.seo_boost_text]
        if self.feed_record.show_news_source:
            parts.append(self.news_source)
        if self.seo_boost_static_url:
            parts.append(self.seo_boost_static_url)
        return self._format(parts)


class ExtraMsgSecondaryConnection(BaseExtraMsg):
    def build_msg(self) -> ExtraMsg:
        parts = [self.seo_boost_text]

        if self.seo_boost_static_url:
            parts.append(self.seo_boost_static_url)

        if self.feed_record.show_news_source:
            parts.append(self.news_source)

        parts.append(self.feed_record.url_for_primary_connection)

        return self._format(parts)


class ExtraMsgService:
    def __init__(self, *, feed: FeedSeo, main_connection: bool, news_source: str):
        self.feed = feed
        self.main_connection = main_connection
        self.news_source = news_source

    async def build_msg(self) -> ExtraMsg:
        data = ExtraMsgData(feed_record=self.feed, news_source=self.news_source)

        if self.main_connection:
            return ExtraMsgMainConnection(data).build_msg()

        return ExtraMsgSecondaryConnection(data).build_msg()
