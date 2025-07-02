from src.configs.settings import settings
from faststream.rabbit import RabbitBroker
import pytest

from faststream.rabbit import TestRabbitBroker
from loguru import logger
from src.presentation.amqp_api_formatting.endpoints import format_text

broker = RabbitBroker(settings.RABBITMQ_URL)


@pytest.mark.asyncio
async def test_handle(task_execution_data_entity):
    logger.info("тест начался")
    task_data = task_execution_data_entity()
    logger.info(task_data.model_dump())
    # await format_text(task_data)
    # async with TestRabbitBroker(broker) as br:
    #     await br.publish(task_data, queue="format_text")
    #     format_text.mock.assert_called_once_with(task_data)


# TaskExecutionData(**{
#     "user_id": 1,
#     "feed": {
#         "feed_id": 1,
#         "feed_title": "Stay senior consider less imagine later international set. Floor open hold plan bag operation quality. Agency present over second worker third drop buy. Increase agent rate first.",
#     },
#     "connection": {
#         "connection_id": 1,
#         "connection_name": "Early vote price own yard mind matter. Beautiful opportunity yeah oil financial my own. Push surface lead number particularly suggest arm.\nHere reality common start remain which.",
#         "is_connection_primary": True,
#         "account_id": "Hold real hour range. Break Mrs chair so pressure here administration success. Simply oil pressure up foot central.",
#         "access_token": "That leave option fight spring take. But go cup until prove soon.",
#     },
#     "news": {
#         "title": "Bring fight develop turn term.",
#         "published_date": "1982-02-10",
#         "url": "http://www.moore.com/",
#         "publisher": "Cooper Ltd",
#         "description": "Voice follow parent explain without suggest red. Modern nor plan enough they audience. Arrive here them idea field glass.",
#         "text": "Material official ready view black list off civil. Already service forget new big.",
#         "img": "https://www.parks.com/",
#         "summary": "Protect space often instead personal rich. Wide gr",
#     },
#     "formatting_result": {
#         "text": "Standard member yet sometimes exist century. Move hard six run. Music determine example material wish what big myself.",
#         "video_url": None,
#         "dict_repr": None,
#     },
#     "feed_type": "newsfeed",
# })
