import pytest_asyncio
import pytest
from src.infrastructure.db.manager import AsyncPGManager
from src.infrastructure.db.pool import DB_DSN
from src.configs.logger import setup_logging


@pytest.fixture(autouse=True)
def setup_test_logging():
    setup_logging()


@pytest_asyncio.fixture(scope="function")
async def db_manager():
    manager = AsyncPGManager(DB_DSN)
    await manager.connect()
    yield manager
    await manager.close()


pytest_plugins = [
    "tests.fixtures.domain.entity.common",
]
