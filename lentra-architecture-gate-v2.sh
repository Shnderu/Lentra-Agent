#!/bin/bash
set -e

echo "=== LENTRA ARCHITECTURE DECISION GATE v2 ==="

REPO="/opt/lentra"
cd "$REPO"

############################################
# 1. GIT SAFETY
############################################

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "[FATAL] Not a git repository"
  exit 1
}

BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "[INFO] Branch: $BRANCH"

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo "[FATAL] main/master blocked"
  exit 1
fi

############################################
# 2. CORE STRUCTURE SNAPSHOT
############################################

echo "[INFO] Scanning core structure..."

CORE_EXPECTED=(
  "core/normalization"
  "core/search"
  "core/ranking"
  "core/risk"
  "core/deduplication"
  "core/market_intelligence"
)

for d in "${CORE_EXPECTED[@]}"; do
  if [ ! -d "$d" ]; then
    echo "[FATAL] Missing canonical core module: $d"
    exit 1
  fi
done

############################################
# 3. FORBIDDEN CORE DETECTION
############################################

echo "[INFO] Checking forbidden variants..."

if find core -maxdepth 1 -type d | grep -E "v2|v3|new|copy|alt|backup" >/dev/null 2>&1; then
  echo "[FATAL] FORBIDDEN CORE VARIANT DETECTED"
  exit 1
fi

if find core -type d -name "*advisor*" >/dev/null 2>&1; then
  echo "[FATAL] FORBIDDEN MODULE: advisor"
  exit 1
fi

############################################
# 4. ARCHITECTURE DECISION LOG
############################################

DECISION_LOG=".lentra_context/architecture_decisions.log"

touch "$DECISION_LOG"

############################################
# 5. DECISION GATE CHECK
############################################

echo "[INFO] Checking for architecture mutations..."

CHANGES=$(git status --porcelain core/ | wc -l)

if [ "$CHANGES" -gt 0 ]; then
  echo "[WARNING] Core changes detected"

  echo ""
  echo "CORE MODIFICATIONS:"
  git status --porcelain core/

  echo ""
  echo "⚠️  ARCHITECTURE DECISION REQUIRED"
  echo "You are modifying CORE modules."

  echo ""
  echo "Approve? (type EXACT: APPROVE_CORE_CHANGE)"

  read CONFIRM

  if [ "$CONFIRM" != "APPROVE_CORE_CHANGE" ]; then
    echo "[BLOCKED] No architecture approval"
    exit 1
  fi

  echo "[INFO] Approved core change logged" >> "$DECISION_LOG"
  date >> "$DECISION_LOG"
  git status --porcelain core/ >> "$DECISION_LOG"
fi

############################################
# 6. FINAL OK
############################################

echo "[OK] Architecture gate passed"
