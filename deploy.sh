#!/bin/bash

set -e

cd /opt/flyrum

echo "=== PULL LATEST CODE ==="
git fetch origin
git reset --hard origin/main

echo "=== REBUILD CONTAINERS ==="
docker compose down
docker compose up -d --build

echo "=== DONE ==="
