FROM python:3.10.0-slim-buster

WORKDIR /app

# install requirements
COPY requirements.txt .
RUN apt-get update && \
    pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
