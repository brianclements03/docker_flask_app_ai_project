import os
from app import create_app
from app.services.chromadb_client import collection

def auto_ingest_schema_if_needed():
    """Check if ChromaDB collection is empty, and populate it if so."""
    doc_count = collection.count()
    if doc_count == 0:
        print("🔄 ChromaDB is empty. Running schema ingestion...")
        import scripts.load_schema_to_chroma as loader
        loader.main()
    else:
        print(f"✅ ChromaDB already contains {doc_count} documents.")

# Create the Flask app
app = create_app()

# Optionally load schema into ChromaDB at startup
auto_ingest_schema_if_needed()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)




# # app/run.py
# import os
# from app import create_app

# # 🔌 Optional: ingest schema if collection is empty
# from app.services.chromadb_client import collection

# def auto_ingest_schema_if_needed():
#     if collection.count() == 0:
#         print("🔄 ChromaDB is empty. Running schema ingestion...")
#         import scripts.load_schema_to_chroma as loader
#         loader.main()
#     else:
#         print(f"✅ ChromaDB already contains {collection.count()} documents.")
# # the above is optional to populate the chromadb schema. 

# app = create_app()

# auto_ingest_schema_if_needed()

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5001))
#     app.run(host="0.0.0.0", port=port)
