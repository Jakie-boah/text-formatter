from dishka import Provider, Scope, from_context, provide
from src.configs.settings import Settings
from src.infrastructure.db.manager import AsyncPGManager


class SessionProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_db_manager(self, settings: Settings) -> AsyncPGManager:
        manager = AsyncPGManager(settings.db_dsn)
        await manager.connect()
        return manager
