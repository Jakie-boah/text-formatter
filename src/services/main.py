from src.services.connections import VK, Facebook, Instagram, Telegram, Twitter, Website
from src.services.text import TextFormatter


def get_text_formatter(social: str) -> type[TextFormatter]:
    match social.lower():
        case "telegram":
            return Telegram

        case "facebook":
            return Facebook

        case "instagram":
            return Instagram

        case "website":
            return Website

        case "vk":
            return VK

        case "twitter":
            return Twitter
