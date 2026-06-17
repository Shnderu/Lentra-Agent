#!/bin/bash

set -e

mkdir -p app/core
mkdir -p app/services

touch app/main.py
touch app/core/events.py
touch app/core/event_bus.py
touch app/core/handlers.py
touch app/services/rent_search.py

echo "[OK] folders and base files created"
