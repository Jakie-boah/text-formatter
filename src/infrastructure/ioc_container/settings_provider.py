from dishka import Provider, Scope, provide
from loguru import logger

from src.configs.settings import Settings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_settings(self) -> Settings:
        logger.info("Готово")
        return Settings()
