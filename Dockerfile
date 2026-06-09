FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir aiogram psycopg2-binary redis

CMD ["python", "-u", "main.py"]
