from scripts.extract_schema import extract_schema_docs
from app.services.chroma_ingest import ingest_schema
import time
import requests

def wait_for_chromadb(host="http://localhost", port=8000, retries=10, delay=2):
    url = f"{host}:{port}/api/v2/heartbeat"
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

def main():
    wait_for_chromadb(host="http://chromadb", port=8000)

    print("⏳ Extracting schema...")
    docs = extract_schema_docs()
    print(f"✅ Extracted {len(docs)} schema documents.")
    for doc in docs[:5]:  # Just preview the first few
        print(f"📝 {doc}")

    print("📥 Ingesting into ChromaDB...")
    ingest_schema(docs)

    print("✅ Done.")

# Allows running as a script directly, OR importing `main()` from elsewhere (e.g. run.py)
if __name__ == "__main__":
    main()














# from scripts.extract_schema import extract_schema_docs
# from app.services.chroma_ingest import ingest_schema
# import time
# import requests

# import time
# import requests

# def wait_for_chromadb(host="http://localhost", port=8000, retries=10, delay=2):
#     url = f"{host}:{port}/api/v2/heartbeat"
#     print("⏳ Waiting for ChromaDB to become ready...")

#     for attempt in range(1, retries + 1):
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 print("✅ ChromaDB is ready.")
#                 return
#         except requests.exceptions.ConnectionError:
#             print(f"🔄 Attempt {attempt}/{retries}: ChromaDB not ready yet.")
#         time.sleep(delay)

#     raise RuntimeError("❌ ChromaDB did not become ready in time.")

# wait_for_chromadb(host="http://chromadb", port=8000)

# print("⏳ Extracting schema...")
# docs = extract_schema_docs()
# print(f"✅ Extracted {len(docs)} schema documents.")
# for doc in docs[:5]:  # Just preview the first few for now
#     print(f"📝 {doc}")

# print("📥 Ingesting into ChromaDB...")
# ingest_schema(docs)

# print("✅ Done.")