#!/bin/bash
set -e

echo "=== LENTRA CONTEXT COMPILER v1 ==="

REPO="/opt/lentra"
OUT="$REPO/.lentra_context"

mkdir -p "$OUT"

echo "[1] core context"
cat > "$OUT/core_context.md" <<'CTX'
# CORE CONTEXT

core/normalization
core/search
core/ranking
core/risk
core/deduplication
core/market_intelligence

RULE:
- single source of truth
- no duplicates
CTX

echo "[2] infra context"
cat > "$OUT/infra_context.md" <<'CTX'
# INFRA CONTEXT

ALLOWED:
- api routing
- pipeline
- http layer

FORBIDDEN:
- business logic
- ranking logic
- search logic
CTX

echo "[3] pipeline context"
cat > "$OUT/pipeline_context.md" <<'CTX'
# PIPELINE

API → Pipeline → Core → Result

RULE:
- no bypass
- no infra logic
CTX

echo "[DONE] context compiled -> $OUT"
