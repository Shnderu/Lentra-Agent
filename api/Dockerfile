FROM lentra-base:latest

WORKDIR /app

ENV PYTHONPATH=/app

COPY core /app/core
COPY api /app/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
