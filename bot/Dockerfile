FROM lentra-base:latest

WORKDIR /app

COPY bot/ /app/bot/
COPY core/ /app/core/

ENV PYTHONPATH=/app

CMD ["python", "bot/main.py"]
