import faker
import pytest
from loguru import logger

from src.db.repository import PromptRepository
from src.services.connections.telegram import Telegram
from src.services.exceptions import MaxCounterError
from src.services.gpt import GPTRequests
from src.services.main import FormattingData, NewsData

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
        GPTRequests,
        "translate_if_necessary",
        mock_translate_if_necessary,
    )


@pytest.mark.asyncio
async def test_text_formatter(news, configs, mocks, db_manager):
    configs.extra_text_after_formatting = "\nExtra MSG\n"
    configs.extra_prompt = "\nSome Extra Prompt\n"
    formatter = Telegram(news=news, configs=configs, db_manager=db_manager)
    repository = PromptRepository(db_manager)
    result = await repository.get_prompt(social="Telegram")

    assert formatter.news == news
    assert formatter.configs == configs
    assert formatter.format_type == configs.format_type

    prompt = await formatter.get_prompt()
    assert prompt == f"{result}\nSome Extra Prompt\n"

    result = await formatter.format()
    logger.info(result)
    assert (
        result
        == f"{news.title}\n\n{news.text + configs.extra_text_after_formatting}\n\n"
    )


@pytest.mark.asyncio
async def test_text_formatter_error_raise(news, configs, mocks, db_manager):
    news.text = "some short text"
    formatter = Telegram(news=news, configs=configs, db_manager=db_manager)
    with pytest.raises(MaxCounterError):
        await formatter.format()
