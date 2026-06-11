FROM python:3.11

WORKDIR /app

COPY worker/ /app/worker/
COPY core/ /app/core/

ENV PYTHONPATH=/app

RUN pip install redis

CMD ["python", "-u", "worker/worker_stream.py"]
