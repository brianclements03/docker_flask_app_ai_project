def build_sql_prompt(user_question: str, schema_snippets: list[str]) -> str:
    schema_text = "\n\n".join(schema_snippets)
    prompt = f"""You are an AI assistant that generates MySQL queries based only on the provided schema.

SCHEMA:
{schema_text}

QUESTION:
{user_question}

RULES:
- Use only the tables and columns shown in the schema above.
- Do not guess or invent any tables or columns.
- If the question cannot be answered using only this schema, reply with: "Insufficient schema information."

Respond with ONLY the SQL query. No commentary, no explanation.
"""
    return prompt
