import chromadb
from chromadb.config import Settings

# Optional: change host/port if not default
CHROMA_SETTINGS = Settings(
    chroma_api_impl="rest",
    chroma_server_host="localhost",
    chroma_server_http_port=8000
)

client = chromadb.Client(CHROMA_SETTINGS)

# Create or get collection
collection_name = "docs"
collection = client.get_or_create_collection(name=collection_name)

# Add sample data (optional — for dev/testing)
collection.add(
    documents=["The quick brown fox jumps over the lazy dog."],
    metadatas=[{"source": "init"}],
    ids=["doc1"]
)

print(f"✅ Initialized ChromaDB collection '{collection_name}' with test doc.")
