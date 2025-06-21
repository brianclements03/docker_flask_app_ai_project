# scripts/extract_schema.py
from sqlalchemy import create_engine, inspect
import os

def extract_schema_docs():
    # Use your container settings
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "supersecurepassword")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3307")  # match Docker binding
    DB_NAME = os.getenv("DB_NAME", "ai_chatbot_db")

    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)
    inspector = inspect(engine)

    schema_docs = []

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        for col in columns:
            col_name = col['name']
            col_type = str(col['type'])
            doc_text = f"Column '{col_name}' in table '{table_name}' of type {col_type}"
            doc_id = f"{table_name}_{col_name}"
            schema_docs.append({
                "id": doc_id,
                "content": doc_text
            })

    return schema_docs

# Optional test run
if __name__ == "__main__":
    docs = extract_schema_docs()
    for d in docs[:5]:
        print(d)
