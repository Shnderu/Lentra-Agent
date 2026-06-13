# ============================================================
# LENTRA DOCKER V17.2
# ============================================================

FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn asyncio

CMD ["python", "-m", "lentra.api.main"]
