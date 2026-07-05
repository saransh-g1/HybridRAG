from app.services.sql.sql_generator import get_sql_generator

generator = get_sql_generator()

print(
    generator.generate(
        "How many documents are indexed?"
    )
)