from faststream.rabbit import RabbitMessage, RabbitQueue, RabbitRouter, RabbitBroker
from faststream.rabbit.schemas.queue import QueueType
from loguru import logger
from dishka import FromDishka
from dishka.integrations.faststream import inject
from src.domain.entities.common import TaskExecutionData
from src.application.interactors.text_format_interactor import TextInteractor

endpoints = RabbitRouter(include_in_schema=True)


@endpoints.subscriber(
    queue=RabbitQueue(
        name="himmera_format_text",
        durable=True,
        passive=False,
        routing_key="himmera_format_text",
        queue_type=QueueType.QUORUM,
    ),
    no_ack=False,
    retry=False,
)
@inject
async def format_text(
    payload: TaskExecutionData,
    msg: RabbitMessage,
    interactor: FromDishka[TextInteractor],
    broker: FromDishka[RabbitBroker],
):
    logger.info(
        f"получил задачу на форматирование текста для Feed(id={payload.feed_id}, user_id={payload.user_id})"
    )

    text = await interactor(payload)
    logger.info(f"Выполнено форматирование - полученный текст\n\n{text}")

    formatting_result = {"text": text}
    payload.formatting_result = formatting_result

    await broker.publish(payload.model_dump(), queue="himmera_publish_post")
    await msg.ack()
