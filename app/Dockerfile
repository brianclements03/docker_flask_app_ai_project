# app/Dockerfile

FROM python:3.11-slim

WORKDIR /flask-app

# 🛡️ Copy Zscaler cert into container
COPY zscaler-root.crt /usr/local/share/ca-certificates/zscaler.crt

# 📦 Install OS packages and update cert store
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && update-ca-certificates

# 📜 Tell Python to use updated cert chain
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# 📁 Now copy the rest of your app AFTER cert is in place
COPY . .

# 🐍 Install dependencies
RUN pip install --upgrade pip && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# 🌐 Flask app port
EXPOSE 5001

# 🔧 Misc. Python env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 👇 Install certifi if not present and override it with system certs (Zscaler trusted)
RUN python -m pip install certifi \
    && CERT_PATH=$(python -m certifi) \
    && ln -sf /etc/ssl/certs/ca-certificates.crt $CERT_PATH


# 👇 Define an environment variable for model cache
ENV SENTENCE_TRANSFORMERS_HOME=/root/.cache/torch/sentence_transformers
#check the container has outbound network access during build
RUN curl -I https://huggingface.co
#pre-download sentence_transformer model inside the container during build
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
RUN test -d /root/.cache/torch/sentence_transformers && echo "✅ Model cached successfully" || echo "❌ Model not found"

# 🚀 Start app with Gunicorn
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} run:app