from services.chromadb_client import collection
import chromadb
from chromadb.utils import embedding_functions

#initialize chroma client
client = chromadb.HttpClient(host="chromadb",port=8000)

#choose or create collection
collection = client.get_or_create_collection(name="schema_docs")

#load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def ingest_schema(docs):
    text = [docs['text'] for doc in docs]
    ids = [doc['id'] for doc in docs]
    metadata = [doc['metatdata'] for doc in docs]

    #compute embeddings
    print("🔢 Embedding schema documents...")
    embeddings = model.encode(texts).tolist()

    print("💾 Adding to Chroma collection...")
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadata
    )
    print("✅ Schema documents embedded and stored.")


#similarity search in Chromadb functionality
from services.chromadb_client import collection

def search_similar(embedding: list, top_k: int = 5)
    """
    Perform a similarity search in ChromaDB using the given embedding.
    """
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results