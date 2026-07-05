from functools import lru_cache
import re

class SQLValidator:

    FORBIDDEN = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
        "MERGE",
        "CALL",
    ]

   def validate(self, sql: str):

    sql = sql.strip()

    if not sql:
        raise ValueError("Empty SQL")

    sql = re.sub(
        r"\s+",
        " ",
        sql,
    )

    upper = sql.upper()

    if not upper.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed.")

    if ";" in upper[:-1]:
        raise ValueError("Multiple SQL statements are not allowed.")

    for keyword in self.FORBIDDEN:
        if re.search(rf"\b{keyword}\b", upper):
            raise ValueError(f"{keyword} is forbidden.")

    return sql

@lru_cache
def get_sql_validator():
    return SQLValidator()