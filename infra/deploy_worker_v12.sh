#!/bin/bash

set -e

echo "[DEPLOY V12] stop old worker"
docker rm -f lentra-worker || true

echo "[DEPLOY V12] start worker v12"
docker run -d \
  --name lentra-worker \
  --network infra_default \
  --env-file /opt/lentra/.env \
  -v /opt/lentra:/app \
  infra-lentra-worker \
  python -u /app/core/worker/sender_v12.py

echo "[DEPLOY V12] done"
