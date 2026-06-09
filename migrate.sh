#!/bin/bash

set -e

echo "[MIGRATE] start"

docker compose run --rm worker python -c "
from migrations.runner import run
run()
"

echo "[MIGRATE] done"
