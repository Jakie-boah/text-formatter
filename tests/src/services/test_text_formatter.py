import pytest
from src.services.connections.telegram import Telegram
from src.services.main import NewsData, FormattingData


@pytest.fixture
def news():
    return NewsData(
        title="title",
        published_date="Th 14 mai",
        url="https://example.com",
        publisher="Yandex",
        description="description",
        text="text to update",
    )


@pytest.fixture
def configs():
    return FormattingData(language="English", format_type="default")


@pytest.mark.asyncio
async def test_text_formatter(news, configs):

    formatter = Telegram(news=news, configs=configs)

    assert formatter.news == news
    assert formatter.configs == configs
    assert formatter.format_type == configs.format_type
