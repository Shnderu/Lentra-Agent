#!/bin/bash

set -e

echo "[DEPLOY] start"

echo "[DEPLOY] infra down"
docker compose down --remove-orphans

echo "[DEPLOY] infra up"
docker compose up -d --build db redis

echo "[WAIT DB]"
sleep 3

docker compose up -d --build worker

echo "[HEALTH CHECK]"
docker logs -f flyrum-worker
