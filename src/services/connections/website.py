from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup, escape

from src.services.text import TextFormatter

env = Environment(
    loader=FileSystemLoader("src/templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


def linebreaksbr(value):
    escaped = escape(value)
    return Markup(escaped.replace("\n", "<br>\n"))  # noqa: S704


env.filters["linebreaksbr"] = linebreaksbr


class Website(TextFormatter):
    MAX_LENGTH = 8000

    async def format(self) -> str:
        prompt = await self.get_prompt()
        adapted_text = await self._get_adapter().adapt(prompt, self.news.text)
        template = env.get_template("index.html")

        return template.render(
            image=self.news.img,
            full_text=adapted_text + self.extra_msg,
            news_source=self.news.url,
        )

    @property
    def max_length(self) -> int:
        return self.MAX_LENGTH

    async def get_prompt(self) -> str:

        website_prompt = await self.prompt_repository.get_prompt(
            social="Website",
            format_type="newsfeed",
        )
        website_prompt += self.extra_prompt
        return website_prompt


class WebsiteArticle(Website):
    async def get_prompt(self) -> str:
        website_prompt = await self.prompt_repository.get_prompt(
            social="Website",
            format_type="article",
        )
        website_prompt += self.extra_prompt
        return website_prompt


class WebsiteVideo(Website):
    async def get_prompt(self) -> str:
        website_prompt = await self.prompt_repository.get_prompt(
            social="Website",
            format_type="video",
        )
        website_prompt += self.extra_prompt
        return website_prompt
