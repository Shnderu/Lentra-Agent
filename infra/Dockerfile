FROM python:3.10-slim

WORKDIR /opt/lentra/infra

RUN pip install --no-cache-dir \
    sqlalchemy \
    psycopg2-binary \
    pyrogram \
    tgcrypto \
    fastapi \
    uvicorn

COPY . /opt/lentra/infra
