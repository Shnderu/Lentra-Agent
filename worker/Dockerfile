FROM lentra-base:latest

WORKDIR /app

ENV PYTHONPATH=/app

COPY core /app/core
COPY worker /app/worker

CMD ["python", "-u", "worker/worker.py"]
