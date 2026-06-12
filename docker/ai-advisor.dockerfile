FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir redis

COPY core/healing/ /app/core/healing/

CMD ["python", "-u", "/app/core/healing/ai_advisor.py"]
