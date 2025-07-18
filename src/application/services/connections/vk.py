from src.application.services.text import TextFormatter


class VK(TextFormatter):

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

        vk_prompt = await self.prompt_repository.get_prompt(
            social="VK",
            format_type="newsfeed",
        )
        vk_prompt += self.extra_prompt
        return vk_prompt


class VKArticle(VK):
    async def get_prompt(self) -> str:

        vk_prompt = await self.prompt_repository.get_prompt(
            social="VK",
            format_type="article",
        )
        vk_prompt += self.extra_prompt
        return vk_prompt


class VKVideo(VK):
    async def get_prompt(self) -> str:

        vk_prompt = await self.prompt_repository.get_prompt(
            social="VK",
            format_type="video",
        )
        vk_prompt += self.extra_prompt
        return vk_prompt
