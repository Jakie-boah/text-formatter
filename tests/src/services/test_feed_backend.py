import pytest
from src.application.services.feed_backend import FeedBackend
from loguru import logger


@pytest.mark.asyncio
async def test_feed_backend():
    result = await FeedBackend.get_formatting_data_for_feed(feed_id=627)
    logger.info(result)
