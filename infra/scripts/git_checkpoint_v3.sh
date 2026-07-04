#!/usr/bin/env bash

set -e

cd /opt/lentra/infra

echo "[CHECKPOINT] Staging changes..."

git add -A

TAG="rollback_before_area_engine_$(date +%Y%m%d_%H%M%S)"

echo "[CHECKPOINT] Creating tag: $TAG"

git commit -m "$TAG" || echo "[SKIP] nothing to commit"

git tag $TAG || true

echo "[CHECKPOINT] DONE -> $TAG"
