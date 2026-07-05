from functools import lru_cache

from app.services.llm_service import LLMService
from app.services.sql.schema_service import get_schema_service
from app.services.sql.prompts import SQL_SYSTEM_PROMPT


class SQLGenerator:

    def __init__(self):

        self.llm = LLMService()

        self.schema = get_schema_service()

    def generate(self, question: str):

        schema = self.schema.format_schema()

        prompt = f"""
                Database Schema

                {schema}

                Question

                {question}

                SQL:
                """

        sql = self.llm.generate(
            prompt=prompt,
            system_prompt=SQL_SYSTEM_PROMPT,
        )

        return sql.strip()


@lru_cache
def get_sql_generator():

    return SQLGenerator()