import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFuntion

#use the same embedding model as the user question
embedding_fn = SentenceTransformerEmbeddingFuntion(model_name="all-MiniLM-L6-v2")

client = chromadb.HttpClient(host="chromadb", port=8000) #adjust for localhost
collection = client.get_or_create_collection(
    name="schema_elements",
    embedding_function=embedding_fn
)