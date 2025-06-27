import pytest
from loguru import logger

from src.infrastructure.db.repository import PromptRepository


@pytest.mark.asyncio
@pytest.mark.parametrize("type_", ["newsfeed", "article", "video", "summarized"])
async def test_repository(db_manager, type_):
    repository = PromptRepository(db_manager)
    result = await repository.get_prompt(social="Telegram", format_type=type_)
    logger.info(result)
