

def build_sql_prompt(user_question: str, schema_snippets: list[str]) -> str:
    schema_text = "\n\n".join(schema_snippets)
    prompt = f"""You are a helpful and knowledgeable SQL generator.

Use the following database schema to write a SQL query that answers the user's question.

SCHEMA:
{schema_text}

QUESTION:
{user_question}

Respond with **only** the SQL query, no explanation. If you don't know the answer or have a good approximation, reply that
the given question can't be answered using the information provided.
"""
    return prompt