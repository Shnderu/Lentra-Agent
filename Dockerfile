FROM python:3.11-slim

WORKDIR /app

# важно: фиксируем корень импортов
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "core.worker.main"]
