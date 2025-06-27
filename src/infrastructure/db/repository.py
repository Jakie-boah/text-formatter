from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from src.infrastructure.db.queries import PromptQueries


class Repository(ABC):
    @abstractmethod
    async def get(self, **kwargs):
        pass


class BasePromptRepository(Repository):
    def __init__(self, db_manager):
        self.db = db_manager
        self.queries = PromptQueries()

    async def get(self, *, social, prompt_type) -> str | None:
        row = await self.db.fetchrow(
            self.queries.get_prompt, social, prompt_type,
        )
        if row:
            return row["prompt"]
        return None


class PromptRepository(BasePromptRepository):
    async def get_prompt(
        self,
        *,
        social,
        format_type: Literal["summarized", "article", "newsfeed", "video"] = "newsfeed",
    ) -> str | None:
        return await self.get(social=social, prompt_type=format_type)
