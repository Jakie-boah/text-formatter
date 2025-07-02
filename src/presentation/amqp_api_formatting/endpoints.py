from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitMessage, RabbitQueue, RabbitRouter, RabbitBroker
from faststream.rabbit.schemas.queue import QueueType
from loguru import logger

endpoints = RabbitRouter(include_in_schema=True)


@endpoints.subscriber(
    queue=RabbitQueue(
        name="format_text",
        durable=True,
        passive=False,
        routing_key="format_text",
        queue_type=QueueType.QUORUM,
    ),
    no_ack=False,
    retry=False,
)
@inject
async def format_text(
    payload,
    msg: RabbitMessage,
    broker: FromDishka[RabbitBroker],
):
    logger.info("ЙОУ")
    logger.info(payload)
    # await broker.publish(message="etsttetttte kdsfsd", queue="publish_post")
