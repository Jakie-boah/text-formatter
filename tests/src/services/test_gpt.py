import pytest
from src.services.gpt import GPTRequests


@pytest.mark.asyncio
async def test_translation():
    """проверяем просто что запрос опену идет и все окей - результаты не так важны"""

    language2translate = "english"
    text = "Россия, Путин, Москва, Спартак - ДОМ"
    result = await GPTRequests(language=language2translate).translate_if_necessary(
        text=text
    )
    assert result != text
    assert result == "Oops couldn't generate text"


@pytest.mark.asyncio
async def test_adapt_text():
    """проверяем просто что запрос опену идет и все окей - результаты не так важны"""

    language2translate = "english"
    text = "Россия, Путин, Москва, Спартак - ДОМ"
    result = await GPTRequests(language=language2translate).adapt_text(
        prompt="Some prompt", text=text
    )
    assert result != text
    assert result == "Oops couldn't generate text"
