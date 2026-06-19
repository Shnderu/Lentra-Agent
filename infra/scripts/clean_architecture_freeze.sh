#!/bin/bash

set -e

echo "[FREEZE] starting architecture freeze..."

# -----------------------------
# 1. DISABLE LEGACY SYSTEMD UNITS
# -----------------------------
echo "[FREEZE] disabling legacy services..."

systemctl disable lentra.service || true
systemctl stop lentra.service || true

systemctl disable lentra-consumer.service || true
systemctl stop lentra-consumer.service || true

# orchestrator is NOT a systemd unit, but we block its execution surface
echo "[FREEZE] legacy systemd cleanup done"

# -----------------------------
# 2. MASK OPTIONAL/LEGACY UNITS (HARD BLOCK)
# -----------------------------
systemctl mask lentra.service || true
systemctl mask lentra-consumer.service || true

# -----------------------------
# 3. CLEAN ORPHAN RUNTIME PID FILES
# -----------------------------
echo "[FREEZE] cleaning orphan PID files..."

rm -f /tmp/lentra_api.pid || true
rm -f /tmp/lentra_ui.pid || true

# -----------------------------
# 4. STOP ANY ORPHAN PROCESSES (SAFETY NET)
# -----------------------------
echo "[FREEZE] killing legacy processes..."

pkill -f "app.ui.server" || true
pkill -f "app.api.server" || true
pkill -f "run.consumer" || true
pkill -f "orchestrator" || true

# -----------------------------
# 5. VERIFY ONLY CURRENT RUNTIME
# -----------------------------
echo "[FREEZE] verifying active services..."

systemctl status lentra-api.service --no-pager || true
systemctl status lentra-bot.service --no-pager || true
systemctl status lentra-worker.service --no-pager || true

# -----------------------------
# 6. FINAL STATE REPORT
# -----------------------------
echo "[FREEZE] active python processes:"
ps aux | grep -E "lentra|uvicorn|worker.engine|telegram" | grep -v grep || true

echo "[FREEZE] DONE. Architecture locked to single runtime layer."
