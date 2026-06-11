FROM lentra-python-base:latest

WORKDIR /app

COPY bot/ /app/bot/
COPY core/ /app/core/

ENV PYTHONPATH=/app

CMD ["python", "-u", "bot/main.py"]
