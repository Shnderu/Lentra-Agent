cat > /opt/flyrum/ARCHITECTURE.md << 'EOF'
# FlyRum Single Source Architecture

## RULE #1 — One Entry Point Per Service
- bot → bot/main.py
- worker → workers/worker.py
- db → postgres only (no logic)

## RULE #2 — NO DUPLICATE SOURCES
Запрещено:
- core/db.py дублирующий connection.py
- multiple queue implementations
- legacy task_queue usage

## RULE #3 — SINGLE QUEUE SYSTEM
ONLY:
core/engine/postgres_queue.py

NO:
redis queue, in-memory queue, task_queue legacy

## RULE #4 — IMPORT RULE
All imports MUST follow:

from core.<module>

NO relative fallback logic

## RULE #5 — DB SCHEMA IS SOURCE OF TRUTH
Tables:
- tasks (mandatory)
No silent creation in code

## RULE #6 — DOCKER IS FINAL LAYER
All runtime configuration ONLY in docker-compose.yml

No hidden env overrides
EOF
