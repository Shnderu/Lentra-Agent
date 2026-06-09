FROM python:3.11-slim

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir \
    psycopg2-binary \
    redis \
    aiogram

CMD ["python", "-u", "/app/main.py"]
