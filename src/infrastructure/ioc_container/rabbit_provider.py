from dishka import Provider, Scope, from_context, provide
from faststream.rabbit import RabbitBroker

from src.configs.settings import Settings


class RabbitProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_rabbit_broker(self, settings: Settings) -> RabbitBroker:
        return RabbitBroker(settings.RABBITMQ_URL)
