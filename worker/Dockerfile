FROM lentra-base:latest

WORKDIR /app

COPY worker/ /app/worker/
COPY core/ /app/core/

ENV PYTHONPATH=/app

CMD ["python", "-u", "worker/worker.py"]
