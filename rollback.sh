#!/bin/bash

echo "[ROLLBACK START]"

docker compose down -v

echo "[RESET DB VOLUME]"
docker volume rm flyrum_flyrum_db 2>/dev/null || true

echo "[RESTORE PREVIOUS STATE NOT IMPLEMENTED YET]"
echo "[TIP] use backups or snapshots"

echo "[DONE]"
