import asyncpg
import pytest

from src.infrastructure.db.manager import AsyncPGManager
from src.infrastructure.db.pool import DB_DSN


@pytest.mark.asyncio
async def test_asyncpg_manager_lifecycle():
    manager = AsyncPGManager(DB_DSN)
    await manager.connect()
    assert isinstance(manager._pool, asyncpg.Pool)

    result = await manager.fetchrow("SELECT 1 as test_col")
    assert result["test_col"] == 1

    await manager.close()
    assert manager._pool is None
