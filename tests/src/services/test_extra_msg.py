import pytest
from src.services.extra_msg import (
    ExtraMsgMainConnection,
    ExtraMsgSecondaryConnection,
    ExtraMsgService,
)
from src.models.feed import SeoBoost, NewsFeed, ExtraMsgData
from tests.src.services.test_text_formatter import news


@pytest.fixture()
def seo_boost_config():
    return SeoBoost(
        link_to_full_news=True, text="some text test", static_url="example.com"
    )


@pytest.fixture()
def extra_msg(seo_boost_config, news):
    newsfeed = NewsFeed(
        primary_logic=True,
        feed_connections_length=1,
        seo_boost=seo_boost_config,
        show_news_source=True,
        url_for_primary_connection="bla.com",
    )
    return ExtraMsgData(feed_record=newsfeed, news=news())


@pytest.mark.asyncio
async def test_extra_seo_boost_msg_main_connection(extra_msg):
    extra_msg_service = ExtraMsgMainConnection(data=extra_msg)
    result = extra_msg_service.build_msg()

    expected = f"\n{extra_msg.feed_record.seo_boost.text}\n{extra_msg.news.url}\n"
    assert result == expected


@pytest.mark.asyncio
async def test_extra_seo_boost_msg_main_connection_false(extra_msg):
    extra_msg_service = ExtraMsgSecondaryConnection(data=extra_msg)
    result = extra_msg_service.build_msg()
    expected = f"\n{extra_msg.feed_record.seo_boost.text}\n{extra_msg.feed_record.seo_boost.static_url}\n"

    assert result == expected

    extra_msg.feed_record.seo_boost.static_url = ""
    extra_msg_service = ExtraMsgSecondaryConnection(data=extra_msg)
    result = extra_msg_service.build_msg()
    expected = f"\n{extra_msg.feed_record.seo_boost.text}\n{extra_msg.feed_record.url_for_primary_connection}\n"
    assert result == expected


@pytest.mark.asyncio
async def test_extra_msg_se_boost_empty(extra_msg):
    extra_msg.feed_record.seo_boost = None
    extra_msg_service = ExtraMsgMainConnection(data=extra_msg)
    result = extra_msg_service.build_msg()
    assert result == f"\n{extra_msg.news.url}\n"

    extra_msg_service = ExtraMsgSecondaryConnection(data=extra_msg)
    result = extra_msg_service.build_msg()
    assert result == f"\n{extra_msg.feed_record.url_for_primary_connection}\n"


@pytest.mark.asyncio
async def test_extra_msg_service():
    await ExtraMsgService(feed_id=999, status=True, news=news()).build_msg()
