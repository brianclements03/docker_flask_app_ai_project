import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "database": os.getenv("DB_NAME", "ai_chatbot_db"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

try:
    print("🔗 Connecting to MySQL...")
    conn = mysql.connector.connect(**db_config)
    print("✅ MySQL connection successful.")
except mysql.connector.Error as err:
    print(f"❌ Connection failed: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
