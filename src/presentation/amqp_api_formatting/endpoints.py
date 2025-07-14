from dishka import FromDishka
from dishka.integrations.faststream import inject
from faststream.rabbit import RabbitMessage, RabbitQueue, RabbitRouter, RabbitBroker
from faststream.rabbit.schemas.queue import QueueType
from loguru import logger
from pydantic import BaseModel, Field, NonNegativeInt

endpoints = RabbitRouter(include_in_schema=True)


class UserInfo(BaseModel):
    name: str = Field(..., examples=["John"], description="Registered user name")
    user_id: NonNegativeInt = Field(..., examples=[1], description="Registered user id")


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
    user: UserInfo,
    msg: RabbitMessage,
    broker: FromDishka[RabbitBroker],
):
    logger.info("ЙОУ")
    logger.info(user)
    assert user.name == "John"
    assert user.user_id == 1
    await broker.publish(message="etsttetttte kdsfsd", queue="publish_post")
