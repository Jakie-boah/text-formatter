import faker
import pytest
from loguru import logger

from src.services.exceptions import MaxCounterError
from src.services.gpt import GPTRequests
from src.models.news import NewsData, FormattingData
from src.db.repository import PromptRepository
from src.services.connections import *

fake = faker.Faker()


@pytest.fixture
def news():
    def _create_news(desired_length: int = 2200) -> NewsData:
        text = ""
        while len(text) < desired_length:
            text += fake.paragraph() + "\n\n"
        text = text[:desired_length]
        return NewsData(
            title="title",
            published_date="Th 14 mai",
            url="https://example.com",
            publisher="Yandex",
            description="description",
            text=text,
        )

    return _create_news


@pytest.fixture
def configs():
    return FormattingData(language="English", format_type="default")


@pytest.fixture
def mocks(monkeypatch):
    async def mock_adapt_text(self, prompt, text):
        return text

    async def mock_translate_if_necessary(self, text):
        return text

    async def mock_get_prompt(self, *, social, format_type):
        return f"Prompt for {social}"

    monkeypatch.setattr(GPTRequests, "adapt_text", mock_adapt_text)
    monkeypatch.setattr(
        GPTRequests,
        "translate_if_necessary",
        mock_translate_if_necessary,
    )
    monkeypatch.setattr(PromptRepository, "get_prompt", mock_get_prompt)


@pytest.mark.asyncio
async def test_text_formatter(news, configs, mocks, db_manager):
    news = news()
    configs.extra_text_after_formatting = "\nExtra MSG\n"
    configs.extra_prompt = "\nSome Extra Prompt\n"
    formatter = Telegram(news=news, configs=configs, db_manager=db_manager)
    repository = PromptRepository(db_manager)
    result = await repository.get_prompt(social="Telegram", format_type="default")

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
    news = news()
    news.text = "some short text"
    formatter = Telegram(news=news, configs=configs, db_manager=db_manager)
    with pytest.raises(MaxCounterError):
        await formatter.format()


@pytest.mark.asyncio
async def test_twitter_formatting(news, configs, mocks, db_manager):
    news = news(280)
    formatter = Twitter(news=news, configs=configs, db_manager=db_manager)
    assert formatter.max_length == 280
    result = await formatter.format()
    logger.info(result)
    assert (
        result
        == f"{news.title}\n\n{news.text + configs.extra_text_after_formatting}\n\n"
    )


@pytest.mark.asyncio
async def test_twitter_formatting_different_length(news, configs, mocks, db_manager):
    news = news(280)
    configs.extra_text_after_formatting = "\nExtra MSG\n"
    formatter = Twitter(news=news, configs=configs, db_manager=db_manager)
    assert formatter.max_length == 280 - len(configs.extra_text_after_formatting) - 10


@pytest.mark.asyncio
async def test_website_format(news, configs, mocks, db_manager):
    news = news(5000)
    configs.extra_prompt = "\nExtra Prompt\n"
    configs.extra_text_after_formatting = ""  # Website шаблон сам управляет этим
    formatter = Website(news=news, configs=configs, db_manager=db_manager)

    prompt = await formatter.get_prompt()
    assert prompt == "Prompt for Website\nExtra Prompt\n"

    html = await formatter.format()
    logger.info(html)

    # Проверяем, что HTML содержит основные вставки
    assert '<div class="neuron-wrapper">' in html
    assert news.url in html
    assert news.text[:50] in html or news.text[-50:] in html
