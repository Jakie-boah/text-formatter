import pytest_asyncio

from src.db.manager import AsyncPGManager
from src.db.pool import DB_DSN


@pytest_asyncio.fixture(scope="function")
async def db_manager():
    manager = AsyncPGManager(DB_DSN)
    await manager.connect()
    yield manager
    await manager.close()
