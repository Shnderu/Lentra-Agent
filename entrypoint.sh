#!/bin/sh

echo ">>> FLYRUM ENTRYPOINT START"
echo ">>> SERVICE=$SERVICE"

if [ "$SERVICE" = "bot" ]; then
  echo ">>> BOT STARTED"
  python main.py

elif [ "$SERVICE" = "worker" ]; then
  echo ">>> WORKER STARTED"
  python worker.py

elif [ "$SERVICE" = "scheduler" ]; then
  echo ">>> SCHEDULER STARTED"
  python scheduler.py

else
  echo "UNKNOWN SERVICE"
  exit 1
fi
