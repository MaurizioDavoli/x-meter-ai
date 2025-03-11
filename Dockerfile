FROM python:3.10.0-slim-buster

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

WORKDIR /app

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["bash", "/app/entrypoint.sh"]
