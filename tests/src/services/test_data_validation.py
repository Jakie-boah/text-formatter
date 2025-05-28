import asyncio
import json
import os

import aiohttp
import pytest
from dotenv import load_dotenv
from loguru import logger

from src.services.text import FormattingData, NewsData

HEADERS = {"X-API-Key": os.environ.get("NEURON_SERVER_KEY")}


async def check_task(task_id):
    while True:
        url = os.environ.get("SERVER", "https://api.neuron.expert/") + "task/checkTask"
        param = {"uuid": task_id}

        await asyncio.sleep(1.5)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS, params=param) as response:
                assert response.status == 200

                response = await response.json()

                logger.info(response)

                if response["status"] == "done":

                    return NewsData(**json.loads(response["result"]["result"]))

                if response["status"] == "failed":
                    return "Failed"


@pytest.mark.asyncio
async def test_formatting_data():
    data = FormattingData(language="en", extra_text_after_formatting="Hello", extra_prompt="bla")
    assert data.extra_text_after_formatting == "\nHello\n"
    assert data.extra_prompt == "\nbla\n"


@pytest.mark.asyncio
@pytest.mark.skip
async def test_data_validation_newsfeed():
    load_dotenv(dotenv_path="../../../.env")

    headers = {"X-API-Key": os.getenv("NEURON_SERVER_KEY")}
    url = os.getenv("PROD_URL") + "metaconnect/newsfeed"

    async with aiohttp.ClientSession() as session:
        json = {"newsfeed": 595, "news_type": 1}
        async with session.post(url, json=json, headers=headers) as response:
            assert response.status == 200

            data = await response.json()
            task_id = data["taskId"]
            logger.info(task_id)

    result = await check_task(task_id)

    assert isinstance(result, NewsData)


@pytest.mark.asyncio
@pytest.mark.skip
async def test_data_validation_article():
    load_dotenv(dotenv_path="../../../.env")

    headers = {"X-API-Key": os.getenv("NEURON_SERVER_KEY")}
    url = os.getenv("PROD_URL") + "metaconnect/articlesfeed"

    async with aiohttp.ClientSession() as session:
        json_ = {"article_type": 1, "articlesfeed": 610}
        async with session.post(url, json=json_, headers=headers) as response:
            assert response.status == 200

            data = await response.json()
            task_id = data["taskId"]
            logger.info(task_id)

    result = await check_task(task_id)

    assert isinstance(result, NewsData)
