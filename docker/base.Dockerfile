FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# системные зависимости (минимальные)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# единый requirements слой (ВАЖНО: общий для всех сервисов)
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt
