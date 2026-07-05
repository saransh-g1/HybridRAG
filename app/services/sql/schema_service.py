from functools import lru_cache

from sqlalchemy import inspect

from app.db.session import engine


class SchemaService:

    def __init__(self):
        self.inspector = inspect(engine)

    def get_schema(self):

        schema = []

        tables = self.inspector.get_table_names()

        for table in tables:

            columns = self.inspector.get_columns(table)

            schema.append(
                {
                    "table": table,
                    "columns": [
                        column["name"]
                        for column in columns
                    ],
                }
            )

        return schema

    def format_schema(self):

        schema = self.get_schema()

        text = ""

        for table in schema:

            text += f"Table: {table['table']}\n"

            text += "Columns:\n"

            for column in table["columns"]:
                text += f"- {column}\n"

            text += "\n"

        return text


@lru_cache
def get_schema_service():
    return SchemaService()