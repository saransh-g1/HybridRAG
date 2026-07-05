from openai import OpenAI

from app.config.settings import settings


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_BASE_URL,
        )

    def generate(self, prompt: str, system_prompt: str | None = None,):

        messages=[]
        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            max_tokens=512,
            temperature=0,
        )

        print(response.model_dump_json(indent=2))

        if not response.choices:
            raise RuntimeError(f"LLM returned no choices: {response}")

        return response.choices[0].message.content  