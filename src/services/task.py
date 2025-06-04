from src.services.extra_msg import ExtraMsgService
from src.services.main import get_text_formatter


def example():
    text = ExtraMsgService().build_msg()
    get_text_formatter(text,)
