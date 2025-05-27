import pytest
from loguru import logger

from src.db.repository import PromptRepository


@pytest.mark.asyncio
async def test_repository(db_manager):
    repository = PromptRepository(db_manager)
    result = await repository.get_prompt(social="Telegram")
    logger.info(result)
