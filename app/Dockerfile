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

# 🚀 Start app with Gunicorn
CMD gunicorn --bind 0.0.0.0:${PORT:-5000} run:app