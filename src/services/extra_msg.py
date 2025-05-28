import dataclasses
from src.models.feed import NewsFeed
from src.models.news import NewsData


@dataclasses.dataclass
class ExtraMsgData:
    user_id: str | int
    feed_text: str
    feed_record: NewsFeed
    show_news_source: bool
    news: NewsData


class FooterConstructor:
    def __init__(self, feed_record: NewsFeed, news_dict: NewsData):
        self.feed_record = feed_record
        self.news_dict = news_dict
        self.show_news_source = feed_record.show_news_source
        self.seo_boost = feed_record.seo_boost

        if self.seo_boost:
            self.seo_text = self.seo_boost.text or ""
            self.static_url = self.seo_boost.static_url or ""

    def build_footer(self, main_connection: bool):
        if not self.seo_boost:
            # seo_boost отсутствует — не строим футер
            return ""

        if not main_connection:
            redirect_url = (
                self.static_url or self.feed_record.url_for_primary_connection
            )
            news_url = self.news_dict.url if self.show_news_source else ""
            return f"{self.seo_text} {redirect_url} \n\n{news_url}"

        # логика для главного подключения
        if (
            not self.feed_record.primary_logic
            or self.feed_record.feed_connections_length == 1
        ):
            redirect_url = self.static_url
            seo_text = self.seo_text
        else:
            redirect_url = ""
            seo_text = ""

        news_url = self.news_dict.url if self.show_news_source else ""
        return f"{seo_text}{redirect_url}{news_url}"


class ExtraMsg:
    def __init__(self, data: ExtraMsgData):
        self.data = data

    def add_extra_msg(self, main_connection: bool = True):
        footer_constructor = FooterConstructor(
            feed_record=self.data.feed_record,
            news_dict=self.data.news,
        )

        footer_text = footer_constructor.build_footer(main_connection)
        if footer_text:
            return f"{self.data.feed_text}\n\n{footer_text}"
        return self.data.feed_text
