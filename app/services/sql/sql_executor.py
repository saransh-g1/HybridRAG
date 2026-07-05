from functools import lru_cache

from sqlalchemy import text

from app.db.session import SessionLocal


class SQLExecutor:

    def execute(self, sql: str):

        db = SessionLocal()

        try:

            result = db.execute(
                text(sql)
            )

            rows = result.fetchall()

            columns = result.keys()

            return {
                "columns": list(columns),
                "rows": [
                    list(row)
                    for row in rows
                ],
            }

        finally:

            db.close()


@lru_cache
def get_sql_executor():

    return SQLExecutor()