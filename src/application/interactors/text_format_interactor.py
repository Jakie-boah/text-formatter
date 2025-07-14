from src.application.services.extra_msg import ExtraMsgService
from src.domain.entities.common import TaskExecutionData
from loguru import logger
from src.domain.models.news import FormattingData
from src.application.services.main import get_text_formatter
from src.infrastructure.db.manager import AsyncPGManager


class TextInteractor:
    def __init__(self, db_manager: AsyncPGManager):
        self.db_manager = db_manager

    async def __call__(self, task: TaskExecutionData):
        logger.info(task)

        extra_msg = await ExtraMsgService(
            feed=task.feed_seo,
            main_connection=task.connection.is_connection_primary,
            news_source=task.news.url,
        ).build_msg()

        configs = FormattingData(
            language=task.feed.get("language"),
            format_type=task.feed_type,
            extra_prompt=task.feed.get("prompts", {}).get("text_prompt"),
            extra_text_after_formatting=extra_msg,
        )

        formatter = get_text_formatter(social=task.connection.connection_name)(
            news=task.news, configs=configs, db_manager=self.db_manager
        )
        text = await formatter.format()
        return text
