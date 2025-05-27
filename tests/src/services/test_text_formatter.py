import pytest
from src.services.connections.telegram import Telegram
from src.services.main import NewsData, FormattingData
import faker
from src.services.gpt import GPTRequests
from loguru import logger

fake = faker.Faker()


@pytest.fixture
def news():
    text = ""
    desired_length = 2200
    while len(text) < desired_length:
        text += fake.paragraph() + "\n\n"

    return NewsData(
        title="title",
        published_date="Th 14 mai",
        url="https://example.com",
        publisher="Yandex",
        description="description",
        text=text,
    )


@pytest.fixture
def configs():
    return FormattingData(language="English", format_type="default")


@pytest.fixture
def mocks(monkeypatch):
    async def mock_adapt_text(self, prompt, text):
        return text

    async def mock_translate_if_necessary(self, text):
        return text

    monkeypatch.setattr(GPTRequests, "adapt_text", mock_adapt_text)
    monkeypatch.setattr(
        GPTRequests, "translate_if_necessary", mock_translate_if_necessary
    )


@pytest.mark.asyncio
async def test_text_formatter(news, configs, mocks):
    configs.extra_text_after_formatting = "\nExtra MSG\n"
    configs.extra_prompt = "\nSome Extra Prompt\n"
    formatter = Telegram(news=news, configs=configs)

    assert formatter.news == news
    assert formatter.configs == configs
    assert formatter.format_type == configs.format_type

    prompt = await formatter.get_prompt()
    assert prompt == "Some prompt\nSome Extra Prompt\n"

    result = await formatter.format()
    logger.info(result)
    assert (
        result
        == f"{news.title}\n\n{news.text + configs.extra_text_after_formatting}\n\n"
    )


@pytest.mark.asyncio
async def test_text_formatter_error_raise(news, configs, mocks):
    news.text = "some short text"
    formatter = Telegram(news=news, configs=configs)
    with pytest.raises(Exception):
        await formatter.format()
