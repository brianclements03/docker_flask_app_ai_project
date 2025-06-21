#This would be the docker file for my hello world flask app
FROM python:3.9-slim

#set working dir
WORKDIR /flask-app

#copy zscaler cert into container
COPY zscaler-root.crt /usr/local/share/ca-certificates/zscaler.crt

#install OS packages and update cert store
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && update-ca-certificates

#new addition for MySQL usage: add necessary system package
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev
    # && pip install --no-cache-dir -r requirements.txt

#tell pip and python to trust the updated cert bundle
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV PIP_CERT=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

#testing pip install prior to installing requirements. for testing
RUN curl https://pypi.org/simple/flask-sqlalchemy/
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org Flask-SQLAlchemy

#install app dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy application code
COPY . .

#expose port
EXPOSE 5000

#run command when container starts
#CMD ["python", "app.py"] #old command, replaced with below:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"] #middle version of cmd
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]