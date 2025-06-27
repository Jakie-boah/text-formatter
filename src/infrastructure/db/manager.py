from __future__ import annotations

import asyncpg

from src.application.services.exceptions import ErrorMessages


class AsyncPGManager:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._pool: asyncpg.Pool | None = None

    async def connect(self):
        if not self._pool:
            self._pool = await asyncpg.create_pool(dsn=self._dsn)

    async def close(self):
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def acquire(self):
        if not self._pool:
            raise RuntimeError(ErrorMessages.POOL_ERROR.value)
        return await self._pool.acquire()

    async def execute(self, query: str, *args):
        async with self._pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args):
        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args):
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
