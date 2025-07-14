import asyncio

from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka as setup_faststream_ioc
from faststream.asgi import AsgiFastStream, make_ping_asgi
from faststream.rabbit import RabbitBroker

from src.configs.settings import Settings
from src.infrastructure.ioc_container import (
    InteractorProvider,
    RabbitProvider,
    SessionProvider,
    SettingsProvider,
)
from src.presentation.amqp_api_formatting.endpoints import endpoints
from loguru import logger
from src.configs.logger import setup_logging


async def application_factory():
    container = make_async_container(
        SettingsProvider(),
        RabbitProvider(),
        SessionProvider(),
        InteractorProvider(),
        context={Settings: Settings()},
    )

    broker = await container.get(RabbitBroker)
    logger.info(broker)
    broker.include_routers(endpoints)
    app = AsgiFastStream(
        broker,
        title="HIMMERA-FORMATTING",
        version="0.1",
        asyncapi_path="/docs",
        asgi_routes=[
            ("/health", make_ping_asgi(broker, timeout=3.0)),
        ],
    )
    setup_faststream_ioc(
        container=container,
        app=app,
        finalize_container=True,
    )
    run_options = {"host": "0.0.0.0", "port": "8000"}

    await app.run(run_extra_options=run_options)


if __name__ == "__main__":
    setup_logging()
    asyncio.run(application_factory())
