FROM lentra-python-base:latest

WORKDIR /app

COPY core/ /app/core/
COPY worker/ /app/worker/

ENV PYTHONPATH=/app

RUN pip install redis

CMD ["python", "-u", "worker/worker_v66.py"]
