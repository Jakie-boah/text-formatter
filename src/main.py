from loguru import logger

from src.configs.logger import setup_logging
from src.services.extra_msg import ExtraMsgService
from src.services.main import get_text_formatter
from src.models.news import FormattingData, NewsData
from src.db.pool import get_db
from src.services.feed_backend import FeedBackend

setup_logging()


async def format_text(social, feed_id, connection_status, news, formatting_data):
    logger.info(f"Начал форматировать текст для {social}")

    news = NewsData(**news)

    extra_msg = await ExtraMsgService(
        feed_id=feed_id, main_connection=connection_status, news_source=news.url
    ).build_msg()

    configs = FormattingData(**formatting_data)
    configs.extra_text_after_formatting = extra_msg
    prompt = await FeedBackend.get_feed_prompt_data(feed_id=feed_id)
    configs.extra_prompt = prompt.prompt

    SocialFormatter = get_text_formatter(social=social)

    formatter = SocialFormatter(news=news, configs=configs, db_manager=get_db())
    text = await formatter.format()

    return text




