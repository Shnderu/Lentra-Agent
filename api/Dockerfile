FROM lentra-base:latest

WORKDIR /app

COPY api/ /app/api/
COPY core/ /app/core/

ENV PYTHONPATH=/app

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
