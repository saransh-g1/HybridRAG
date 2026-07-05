from functools import lru_cache

from app.services.sql.sql_executor import (
    get_sql_executor,
)

from app.services.sql.sql_generator import (
    get_sql_generator,
)

from app.services.sql.sql_validator import (
    get_sql_validator,
)

from app.services.llm_service import (
    LLMService,
)


class SQLAgent:

    def __init__(self):

        self.generator = get_sql_generator()

        self.validator = get_sql_validator()

        self.executor = get_sql_executor()

        self.llm = LLMService()

    def answer(
        self,
        question: str,
    ):

        sql = self.generator.generate(
            question
        )

        sql = self.validator.validate(
            sql
        )

        result = self.executor.execute(
            sql
        )

        prompt = f"""
Question:

{question}

SQL:

{sql}

Result:

{result}

Answer naturally.
"""

        return self.llm.generate(
            prompt
        )


@lru_cache
def get_sql_agent():

    return SQLAgent()