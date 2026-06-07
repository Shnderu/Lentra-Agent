#!/bin/bash

set -e

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="/opt/backups/$TIMESTAMP"

mkdir -p "$BACKUP_DIR"

echo "[BACKUP] Starting: $TIMESTAMP"

# -------------------------
# 1. PostgreSQL dump
# -------------------------
echo "[BACKUP] Dumping Postgres..."

docker exec flyrum-db pg_dump -U postgres readme_to_recover > "$BACKUP_DIR/db.sql"

# -------------------------
# 2. Redis snapshot
# -------------------------
echo "[BACKUP] Copying Redis dump..."

docker exec flyrum-redis redis-cli SAVE
docker cp flyrum-redis:/data/dump.rdb "$BACKUP_DIR/dump.rdb"

# -------------------------
# 3. Project files
# -------------------------
echo "[BACKUP] Archiving project..."

tar -czf "$BACKUP_DIR/flyrum_project.tar.gz" /opt/flyrum

# -------------------------
# 4. Docker state (optional metadata)
# -------------------------
docker ps -a > "$BACKUP_DIR/docker_ps.txt"
docker images > "$BACKUP_DIR/docker_images.txt"

# -------------------------
# 5. Final archive
# -------------------------
echo "[BACKUP] Creating final archive..."

cd /opt/backups
tar -czf "$TIMESTAMP.tar.gz" "$TIMESTAMP"
rm -rf "$BACKUP_DIR"

echo "[BACKUP] DONE: $TIMESTAMP.tar.gz"
