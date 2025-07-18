from src.application.services.text import TextFormatter


class Telegram(TextFormatter):

    MAX_LENGTH = 4000

    async def format(self):
        prompt = await self.get_prompt()
        adapted_text = await self._get_adapter().adapt(prompt, self.news.text)
        title = await self.gpt.translate_if_necessary(self.title)

        adapted_text = adapted_text + self.extra_msg
        return f"{title}\n\n{adapted_text}\n\n"

    @property
    def max_length(self) -> int:
        return self.MAX_LENGTH

    async def get_prompt(self) -> str:

        telegram_prompt = await self.prompt_repository.get_prompt(
            social="Telegram",
            format_type="newsfeed",
        )
        telegram_prompt += self.extra_prompt
        return telegram_prompt


class TelegramArticle(Telegram):
    async def get_prompt(self) -> str:
        telegram_prompt = await self.prompt_repository.get_prompt(
            social="Telegram",
            format_type="article",
        )
        telegram_prompt += self.extra_prompt
        return telegram_prompt


class TelegramVideo(Telegram):
    async def get_prompt(self) -> str:
        telegram_prompt = await self.prompt_repository.get_prompt(
            social="Telegram",
            format_type="video",
        )
        telegram_prompt += self.extra_prompt
        return telegram_prompt
