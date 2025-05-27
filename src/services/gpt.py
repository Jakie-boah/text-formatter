import os
from functools import wraps

import openai
from loguru import logger

MODEL = "gpt-4.1-mini"

API_KEY = os.environ.get(
    "OPENAI_API_KEY",
    "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",
)

client = openai.AsyncOpenAI(api_key=API_KEY)


def handle_openai_requests(default_error_msg="Oops couldn't generate text"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            try:
                return await func(*args, **kwargs)
            except openai.OpenAIError as e:
                logger.error(f"OpenAI error in {func.__name__}: {e!s}")
                return default_error_msg
            finally:
                await client.close()

        return wrapper

    return decorator


class GPTRequests:

    def __init__(self, language: str):
        self.language = language

    @handle_openai_requests()
    async def adapt_text(self, prompt, text):
        pass

    @handle_openai_requests()
    async def translate_if_necessary(self, text):
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for rewriting texts.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following text with almost no loss of volume into {self.language}. "
                    f"Most important thing, translate it if it is necessary, if given sentence is already written in this language - just return it"
                    f"Just write translated text, thank you",
                },
                {
                    "role": "assistant",
                    "content": f"Could you please provide the text that you would like me to translate "
                    f"with "
                    f"almost no loss of volume into {self.language}? Thank you.",
                },
                {"role": "user", "content": text},
            ],
            temperature=1.0,
        )
        return response.choices[0].message.content.strip()
