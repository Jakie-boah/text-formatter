from src.services.text import TextFormatter


class Instagram(TextFormatter):

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

        insta_prompt = await self.prompt_repository.get_prompt(
            social="Instagram",
            format_type=self.format_type,
        )
        insta_prompt += self.extra_prompt
        return insta_prompt
