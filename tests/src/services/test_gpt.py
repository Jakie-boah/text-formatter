import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.gpt import GPTRequests, client


@pytest.fixture
def gpt_client():
    return GPTRequests(language="en")


@pytest.mark.asyncio
async def test_translate_if_necessary_already_english(gpt_client):
    test_text = "This is already in English"

    with patch.object(
        client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=test_text))]
        )

        result = await gpt_client.translate_if_necessary(test_text)
        assert result == test_text


@pytest.mark.asyncio
async def test_translate_if_necessary_needs_translation(gpt_client):
    original_text = "Bonjour"
    translated_text = "Hello"

    with patch.object(
        client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=translated_text))]
        )

        result = await gpt_client.translate_if_necessary(original_text)
        assert result == translated_text


@pytest.mark.asyncio
async def test_translate_if_necessary_empty_input(gpt_client):
    result = await gpt_client.translate_if_necessary("")
    assert result == ""


@pytest.mark.asyncio
async def test_translate_if_necessary_openai_error(gpt_client):
    with patch.object(
        client.chat.completions, "create", new_callable=AsyncMock
    ) as mock_create:
        mock_create.side_effect = Exception("API error")

        result = await gpt_client.translate_if_necessary("test")
        assert result == "Oops couldn't generate text"


@pytest.mark.asyncio
async def test_client_closed_on_error(gpt_client):
    with patch.object(client, "close", new_callable=AsyncMock) as mock_close:
        with patch.object(
            client.chat.completions, "create", side_effect=Exception("Error")
        ):
            await gpt_client.translate_if_necessary("test")
            mock_close.assert_awaited_once()


@pytest.mark.asyncio
async def test_client_closed_on_success(gpt_client):
    with patch.object(client, "close", new_callable=AsyncMock) as mock_close:
        with patch.object(
            client.chat.completions,
            "create",
            return_value=MagicMock(
                choices=[MagicMock(message=MagicMock(content="test"))]
            ),
        ):
            await gpt_client.translate_if_necessary("test")
            mock_close.assert_awaited_once()
