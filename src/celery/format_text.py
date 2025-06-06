from celery import shared_task
from loguru import logger
from src.services.extra_msg import ExtraMsgService
from src.services.main import get_text_formatter
from src.models.news import NewsData
import asyncio

# TODO: хуйня это не нужно будет


@shared_task
def format_text(feed_id: int, connection_main_status: bool, news_data: dict):

    news_data = NewsData(**news_data)

    async def _build():
        service = ExtraMsgService(
            feed_id=feed_id,
            main_connection=connection_main_status,
            news_source=news_data.url,
        )
        return await service.build_msg()

    extra_msg = asyncio.run(_build())
