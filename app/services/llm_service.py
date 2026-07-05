from openai import OpenAI

from app.config.settings import settings


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Answer only using the provided context.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

        print(response.model_dump_json(indent=2))

        if not response.choices:
            raise RuntimeError(f"LLM returned no choices: {response}")

        return response.choices[0].message.content  