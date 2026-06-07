#!/bin/bash
set -e

echo ">>> FLYRUM ENTRYPOINT START"

# обязательная переменная
if [ -z "$SERVICE" ]; then
  echo "ERROR: SERVICE is not set"
  exit 1
fi

echo "SERVICE=$SERVICE"

case "$SERVICE" in
  worker)
    exec python /app/workers/worker.py
    ;;
  bot)
    exec python /app/bot/main.py
    ;;
  *)
    echo "UNKNOWN SERVICE: $SERVICE"
    exit 1
    ;;
esac
