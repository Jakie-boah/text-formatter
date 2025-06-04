from src.services import connections
from src.services.text import TextFormatter

_FORMATTER_MAP = {
    "text": {
        "telegram": connections.Telegram,
        "facebook": connections.Facebook,
        "instagram": connections.Instagram,
        "website": connections.Website,
        "vk": connections.VK,
        "twitter": connections.Twitter,
    },
    "article": {
        "telegram": connections.TelegramArticle,
        "facebook": connections.FacebookArticle,
        "instagram": connections.InstagramArticle,
        "website": connections.WebsiteArticle,
        "vk": connections.VKArticle,
        "twitter": connections.TwitterArticle,
    },
    "video": {
        "telegram": connections.TelegramVideo,
        "facebook": connections.FacebookVideo,
        "instagram": connections.InstagramVideo,
        "website": connections.WebsiteVideo,
        "vk": connections.VKVideo,
        "twitter": connections.TwitterVideo,
    },
}


def get_text_formatter(social: str) -> type[TextFormatter]:
    return _FORMATTER_MAP["text"][social.lower()]


def get_article_formatter(social: str) -> type[TextFormatter]:
    return _FORMATTER_MAP["article"][social.lower()]


def get_video_formatter(social: str) -> type[TextFormatter]:
    return _FORMATTER_MAP["video"][social.lower()]
