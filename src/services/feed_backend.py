import os
import aiohttp
from loguru import logger
from src.models.feed import NewsFeed, SeoBoost


FEED_BACKEND_URL = (
    os.getenv("PROD_URL", "https://api.neuron.expert/") + "newsfeed-backend/"
)

if "api.neuron.expert" in FEED_BACKEND_URL:
    HEADERS = {"X-API-Key": os.environ.get("NEURON_SERVER_KEY")}
else:
    HEADERS = {}


class FeedBackend:
    @staticmethod
    async def get_formatting_data_for_feed(*, feed_id: int) -> NewsFeed:
        url = f"{FEED_BACKEND_URL}/api/v1/feed/formatting/{feed_id}/"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("Response:", data)
                    seo = None
                    if data["seo_boost"]:
                        seo = SeoBoost(**data["seo_boost"])
                    data.pop("seo_boost")
                    return NewsFeed(seo_boost=seo, **data)
                else:
                    text = await response.text()
                    raise Exception(f"Error {response.status}: {text}")
