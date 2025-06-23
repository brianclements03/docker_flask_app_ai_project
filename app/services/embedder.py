#embed the user's natural language question

from sentence_transformers import SentenceTransformer

# Load model once at module level
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    return model.encode([text])[0]  # Returns 384-d vector
