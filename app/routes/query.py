from flask import Blueprint, request, render_template

query = Blueprint("query", __name__)

@query.route("/query", methods=["POST"])
def generate_sql():
    question = request.form.get("question")

    # TEMP: mock SQL output — this will later call your RAG pipeline
    mock_sql = f"-- Mock SQL generated from: \"{question}\"\nSELECT * FROM customers WHERE state = 'TX';"

    return render_template("index.html", generated_sql=mock_sql)
