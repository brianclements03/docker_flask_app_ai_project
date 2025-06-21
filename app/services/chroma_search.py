from services.chromadb_client import collection

def search_similar_elements(user_question: str, top_k: int = 5):
    return collection.query(
        query_texts=[user_question],
        n_results=top_k
    )