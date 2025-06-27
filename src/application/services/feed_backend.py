import os

import aiohttp
from loguru import logger

from src.domain.models.feed import NewsFeed, SeoBoost, FeedPrompt

FEED_BACKEND_URL = (
    os.getenv("PROD_URL", "https://api.neuron.expert/") + "newsfeed-backend/"
)

HEADERS = (
    {"X-API-Key": os.environ.get("NEURON_SERVER_KEY")}
    if "api.neuron.expert" in FEED_BACKEND_URL
    else {}
)
HTTP_OK = 200


class FeedBackendError(Exception):
    pass


ERROR_MSG = "Error {0}: {1}"


class FeedBackend:
    @staticmethod
    async def get_formatting_data_for_feed(*, feed_id: int) -> NewsFeed:
        url = f"{FEED_BACKEND_URL}/api/v1/feed/formatting/{feed_id}/"

        async with aiohttp.ClientSession() as session, session.get(
            url,
            headers=HEADERS,
        ) as response:

            if response.status == HTTP_OK:
                data = await response.json()
                logger.info("Response:", data)
                seo = None
                if data["seo_boost"]:
                    seo = SeoBoost(**data["seo_boost"])
                data.pop("seo_boost")
                return NewsFeed(seo_boost=seo, **data)
            text = await response.text()
            raise FeedBackendError(ERROR_MSG.format(response.status, text))

    @staticmethod
    async def get_feed_prompt_data(*, feed_id: int):
        url = f"{FEED_BACKEND_URL}/api/v1/feed/prompts/{feed_id}/"

        async with aiohttp.ClientSession() as session, session.get(
            url,
            headers=HEADERS,
        ) as response:

            if response.status == HTTP_OK:
                data = await response.json()
                logger.info("Response:", data)
                data.pop("image_prompt")
                return FeedPrompt(**data)
            text = await response.text()
            raise FeedBackendError(ERROR_MSG.format(response.status, text))
