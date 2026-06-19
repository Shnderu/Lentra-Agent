#!/bin/bash

set -e

echo "[CORE LOCK v2] starting full architecture freeze..."

# -----------------------------
# 1. HARD DISABLE LEGACY SYSTEMD UNITS
# -----------------------------
systemctl disable lentra.service || true
systemctl stop lentra.service || true
systemctl mask lentra.service || true

systemctl disable lentra-consumer.service || true
systemctl stop lentra-consumer.service || true
systemctl mask lentra-consumer.service || true

echo "[CORE LOCK v2] legacy systemd units locked"

# -----------------------------
# 2. REMOVE ORCHESTRATOR RUNTIME SURFACE
# -----------------------------
echo "[CORE LOCK v2] neutralizing orchestrator runtime..."

if [ -f /opt/lentra/infra/app/control/orchestrator.py ]; then
    cp /opt/lentra/infra/app/control/orchestrator.py \
       /opt/lentra/infra/app/control/orchestrator.py.bak

    cat << 'EOL' > /opt/lentra/infra/app/control/orchestrator.py
"""
CORE LOCKED MODULE

This module is disabled in CORE LOCK v2 architecture.

All orchestration responsibilities moved to:
- lentra.api.server (API layer)
- lentra.worker.engine (queue execution layer)
"""
def disabled():
    raise RuntimeError("Orchestrator is disabled in CORE LOCK v2")
EOL
fi

# -----------------------------
# 3. DISABLE UI SERVER ENTRYPOINT
# -----------------------------
echo "[CORE LOCK v2] disabling UI server entrypoint..."

if [ -f /opt/lentra/infra/app/ui/server.py ]; then
    cat << 'EOL' > /opt/lentra/infra/app/ui/server.py
"""
CORE LOCKED UI ENTRYPOINT

UI is now static-only and served via API gateway if needed.
Direct runtime execution disabled.
"""
def disabled():
    raise RuntimeError("UI server disabled in CORE LOCK v2")
EOL
fi

# -----------------------------
# 4. CLEAN PID ARTIFACTS
# -----------------------------
rm -f /tmp/lentra_api.pid || true
rm -f /tmp/lentra_ui.pid || true

# -----------------------------
# 5. ENSURE ONLY CORE SERVICES RUN
# -----------------------------
echo "[CORE LOCK v2] restarting core services..."

systemctl restart lentra-api.service || true
systemctl restart lentra-worker.service || true
systemctl restart lentra-bot.service || true

sleep 2

# -----------------------------
# 6. VERIFY ACTIVE RUNTIME SURFACE
# -----------------------------
echo "[CORE LOCK v2] active processes:"

ps aux | grep -E "uvicorn|worker.engine|telegram.bot" | grep -v grep || true

echo "[CORE LOCK v2] DONE - architecture locked to single execution plane"
