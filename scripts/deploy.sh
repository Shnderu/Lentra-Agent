#!/bin/bash

set -euo pipefail

PROJECT_ROOT="/opt/lentra"
COMPOSE_FILE="$PROJECT_ROOT/infra/docker-compose.yml"

SERVICE="${1:-all}"

echo "[DEPLOY] service=$SERVICE"

cd "$PROJECT_ROOT/infra"

echo "[1/6] remove orphan containers (safe cleanup)"
docker compose -f "$COMPOSE_FILE" down --remove-orphans || true

echo "[2/6] rebuild images"
if [ "$SERVICE" = "all" ]; then
  docker compose -f "$COMPOSE_FILE" build --no-cache
else
  docker compose -f "$COMPOSE_FILE" build --no-cache "$SERVICE"
fi

echo "[3/6] recreate containers"
if [ "$SERVICE" = "all" ]; then
  docker compose -f "$COMPOSE_FILE" up -d --force-recreate
else
  docker compose -f "$COMPOSE_FILE" up -d --force-recreate "$SERVICE"
fi

echo "[4/6] health check (basic)"
sleep 3
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo "[5/6] redis quick check"
docker exec lentra-redis redis-cli PING || true

echo "[6/6] tail logs (worker-stream if exists)"
docker logs --tail 50 lentra-worker-stream 2>/dev/null || true

echo "[DEPLOY DONE]"
