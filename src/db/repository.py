from abc import ABC, abstractmethod
from typing import Literal


class Repository(ABC):
    @abstractmethod
    async def get(self):
        pass


class PromptRepository(Repository):
    def __init__(self, db_manager):
        self.db = db_manager

    async def get(self):
        return "Some prompt"

    async def get_prompt(
        self, social_name: str, format_type: Literal["default", "summarized"],
    ) -> str:
        return await self.get()
