#!/bin/bash

set -e

SERVICE_NAME="lentra-worker"

echo "[DEPLOY] stopping old container if exists..."
docker rm -f $SERVICE_NAME || true

echo "[DEPLOY] starting new container..."

docker run -d \
  --name $SERVICE_NAME \
  --network infra_default \
  --restart unless-stopped \
  --env-file /opt/lentra/.env \
  -v /opt/lentra:/app \
  infra-lentra-worker \
  python -m core.worker.sender_v2

echo "[DEPLOY] done"

docker ps | grep $SERVICE_NAME || true
