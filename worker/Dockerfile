FROM lentra-base:latest

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY worker/ /app/worker/
COPY core/ /app/core/

ENV PYTHONPATH=/app

CMD ["python", "-u", "worker/worker.py"]
