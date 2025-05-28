import pytest
from src.services.main import get_text_formatter
from src.services.connections import (
    VK,
    Facebook,
    Instagram,
    Telegram,
    Twitter,
    Website,
)


@pytest.mark.asyncio
async def test_get_text_formatter():
    expected_classes = {
        "vk": VK,
        "facebook": Facebook,
        "instagram": Instagram,
        "telegram": Telegram,
        "twitter": Twitter,
        "website": Website,
    }

    for name, cls in expected_classes.items():
        formatter_cls = get_text_formatter(name)
        assert formatter_cls is cls or issubclass(formatter_cls, cls)
