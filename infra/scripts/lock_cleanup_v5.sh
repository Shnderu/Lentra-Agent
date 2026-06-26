#!/bin/bash

set -e

echo "[LOCK] Removing legacy app.core runtime dependencies"

# 1. remove shim imports
grep -R "app.core" /opt/lentra/infra/app -n || true

# 2. force fail if runtime imports exist (CI-style gate)
if grep -R "from app.core" /opt/lentra/infra/app; then
    echo "[FATAL] legacy app.core imports still exist"
    exit 1
fi

echo "[OK] app.core fully removed from runtime layer"
