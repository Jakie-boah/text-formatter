from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal
from src.db.queries import PromptQueries


class Repository(ABC):
    @abstractmethod
    async def get(self, **kwargs):
        pass


class BasePromptRepository(Repository):
    def __init__(self, db_manager):
        self.db = db_manager
        self.queries = PromptQueries()

    async def get(self, *, social) -> str | None:
        row = await self.db.fetchrow(
            self.queries.get_prompt,
            social,
        )
        if row:
            return row["prompt"]
        return None


class PromptRepository(BasePromptRepository):
    async def get_prompt(
        self,
        *,
        social,
        format_type: Literal["default", "summarized"] = "default",
    ) -> str | None:

        if format_type in {"default", "summarized"}:
            return await self.get(social=social)
        return None
