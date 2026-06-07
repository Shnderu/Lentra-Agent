FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# системные зависимости (psycopg2 + debug tools)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# зависимости python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# копируем весь проект
COPY . /app

# ВАЖНО: делаем PYTHONPATH стабильным
ENV PYTHONPATH=/app

# правильный запуск worker
CMD ["python", "-u", "workers/worker.py"]
