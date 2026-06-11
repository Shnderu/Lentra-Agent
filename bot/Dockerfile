FROM lentra-base:latest

WORKDIR /app

ENV PYTHONPATH=/app

COPY core /app/core
COPY bot /app/bot

CMD ["python", "bot/main.py"]
