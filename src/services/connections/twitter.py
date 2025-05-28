from src.services.text import TextFormatter


class Twitter(TextFormatter):
    MAX_LENGTH = 280
    extra_cut = 10

    async def format(self):
        prompt = await self.get_prompt()
        adapted_text = await self._get_adapter().adapt(prompt, self.news.text)
        title = await self.gpt.translate_if_necessary(self.title)

        adapted_text = adapted_text + self.extra_msg
        return f"{title}\n\n{adapted_text}\n\n"

    @property
    def max_length(self) -> int:
        if self.extra_msg:
            return self.MAX_LENGTH - len(self.extra_msg) - self.extra_cut
        return self.MAX_LENGTH

    async def get_prompt(self) -> str:

        twitter_prompt = await self.prompt_repository.get_prompt(
            social="Twitter",
            format_type=self.format_type,
        )
        twitter_prompt += self.extra_prompt
        return twitter_prompt
