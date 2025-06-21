from scripts.extract_schema import extract_schema_docs
from services.chroma_ingest import ingest_schema
import time
import requests

import time
import requests

def wait_for_chromadb(host="http://localhost", port=8000, retries=10, delay=2):
    url = f"{host}:{port}/api/v1/heartbeat"
    print("⏳ Waiting for ChromaDB to become ready...")

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ ChromaDB is ready.")
                return
        except requests.exceptions.ConnectionError:
            print(f"🔄 Attempt {attempt}/{retries}: ChromaDB not ready yet.")
        time.sleep(delay)

    raise RuntimeError("❌ ChromaDB did not become ready in time.")

wait_for_chromadb()

print("⏳ Extracting schema...")
docs = extract_schema_docs()

print("📥 Ingesting into ChromaDB...")
ingest_schema(docs)

print("✅ Done.")