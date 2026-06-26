#!/bin/bash
set -e

echo "[WIPE] START LEGACY CLEAN"

ROOT="/opt/lentra/infra/app"

# 1. УБИРАЕМ app.core runtime dependency
echo "[WIPE] removing app.core runtime imports"

grep -R "from app.core" -n $ROOT | cut -d: -f1 | sort -u | while read f; do
  echo "patching $f"
  sed -i 's/from app\.core/from lentra.core/g' "$f" || true
  sed -i 's/import app\.core/import lentra.core/g' "$f" || true
done

# 2. Жёсткий запрет app.core runtime entrypoints
echo "[WIPE] enforcing boundary rules"

cat << 'INNER' > $ROOT/main.py
# LEGACY LOCKED FILE
# DO NOT IMPORT app.core HERE

from lentra.core.event_bus import EventBus
from lentra.core.events import Event
from lentra.core.handlers import handlers
from lentra.core.trace import Span

print("[MAIN] lentra runtime active")
INNER

# 3. cleanup old intent/gateway cross imports
echo "[WIPE] fixing intent/gateway imports"

find /opt/lentra/infra/lentra -type f -name "*.py" | while read f; do
  sed -i 's/app\.core\.intent/lentra.core.intent/g' "$f" || true
  sed -i 's/app\.core\.gateway/lentra.core.gateway/g' "$f" || true
done

echo "[WIPE] DONE"
