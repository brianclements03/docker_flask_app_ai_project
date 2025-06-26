from flask import Blueprint, request, render_template
from app.services.embedder import embed_text
from app.services.chroma_ingest import search_similar
from app.services.prompt_builder import build_sql_prompt
from app.services.ollama_client import query_ollama

query = Blueprint("query", __name__)

@query.route("/query", methods=["POST"])
def generate_sql():
    question = request.form.get("question", "")
    print(f"\n Received question: {question}")

    #step 1: embed user question
    embedding = embed_text(question)
    print(f" Embedding shape: {len(embedding)} dimensions")

    #step 2: query chromadb for similar schema snippets
    results = search_similar(embedding)
    print(f" chroma returned {len(results['documents'][0])} matching snippets")

    #step 3: extract top schema docs (as strings)
    top_docs = results["documents"][0]
    print("Top schema snippets:")
    for doc in top_docs:
        print(f"Top docs are: - {doc.strip()}")

    #step 4: build prompt for SQL generation
    prompt = build_sql_prompt(question, top_docs)
    print("\n Final prompt sent to Ollama: \n")
    print(prompt)

    #step 5: send prompt to Ollama; get sql
    generated_sql = query_ollama(prompt)
    print("\n Generated SQL: \n")
    return render_template("index.html", generated_sql=generated_sql)

    return render_template("index.html", generated_sql=generated_sql)