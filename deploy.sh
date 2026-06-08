#!/bin/bash
set -e

TAG="stable-$(date +%Y%m%d-%H%M%S)"

echo "[DEPLOY] Building images: $TAG"

docker compose build

echo "[DEPLOY] Restarting stack"

docker compose up -d

echo "[DEPLOY] Done: $TAG"
