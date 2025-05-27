from src.services.main import TextFormatter
from loguru import logger
from src.db.repository import PromptRepository


class Telegram(TextFormatter):

    MAX_LENGTH = 4000

    async def format(self):
        adapted_text = await self._adapt_text()
        title = await self.gpt.translate_if_necessary(self.title)

        adapted_text = adapted_text + self.extra_msg
        return f"{title}\n\n{adapted_text}\n\n"

    async def _adapt_text(self):

        prompt = self.get_prompt()

        adapted_text = await self.gpt.adapt_text(prompt, self.news.text)

        counter = 0

        while True:
            if (
                len(adapted_text) > self.MAX_LENGTH
                or len(adapted_text) < self.MAX_LENGTH
            ):
                if counter >= 5:
                    raise Exception(
                        "Превышено кол-во запросов к нейронке - не получилось войти в лимит по кол-ву символов"
                    )

                logger.info(f"Очень большой текст для Telegram - ({len(adapted_text)})")
                logger.info("Прошу сгенерировать еще раз")
                adapted_text = await self.gpt.adapt_text(prompt, self.news.text)
                counter += 1

            else:
                logger.info("Текст вошел по лимиту - все хорошо")
                logger.info(f"Длина текста - {len(adapted_text)} для Telegram")
                break

        return adapted_text

    async def get_prompt(self) -> str:
        # получаю из бд промпт + добавляю сверху разную шляпу

        telegram_prompt = await PromptRepository.get_prompt(
            "Telegram", self.format_type
        )
        telegram_prompt += self.configs.extra_prompt
        return telegram_prompt
