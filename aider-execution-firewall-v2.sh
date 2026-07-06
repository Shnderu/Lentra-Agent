#!/bin/bash
set -e

echo "=== LENTRA AIDER EXECUTION FIREWALL v2 ==="

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

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "[FATAL] BLOCKED: main/master"
  exit 1
fi

############################################
# 2. BASELINE ARCHITECTURE RULE CHECK
############################################

echo "[INFO] Checking core structure integrity..."

ALLOWED_CORE="
core/normalization
core/search
core/ranking
core/risk
core/deduplication
core/market_intelligence
"

############################################
# 3. DETECT NEW CORE DIRECTORIES
############################################

echo "[INFO] Scanning for forbidden core mutations..."

for d in core/*; do
  [ -d "$d" ] || continue

  case "$d" in
    core/normalization) continue ;;
    core/search) continue ;;
    core/ranking) continue ;;
    core/risk) continue ;;
    core/deduplication) continue ;;
    core/market_intelligence) continue ;;
    *)
      echo "[FATAL] FORBIDDEN CORE MODULE DETECTED: $d"
      exit 1
      ;;
  esac
done

############################################
# 4. DETECT DUPLICATE / VARIANT MODULES
############################################

echo "[INFO] Checking for duplicate architecture patterns..."

DUPLICATES=$(find core -type d | grep -E "(_v[0-9]+|_new|_copy|_alt|backup|duplicate)" || true)

if [ ! -z "$DUPLICATES" ]; then
  echo "[FATAL] DUPLICATE MODULE PATTERNS DETECTED:"
  echo "$DUPLICATES"
  exit 1
fi

############################################
# 5. INFRA LEAKAGE CHECK (BUSINESS LOGIC IN INFRA)

echo "[INFO] Checking infra leakage..."

if grep -R "ranking\|risk\|normalization\|search" infra/ >/dev/null 2>&1; then
  echo "[FATAL] BUSINESS LOGIC DETECTED IN INFRA"
  exit 1
fi

############################################
# 6. PIPELINE INTEGRITY CHECK

echo "[INFO] Checking pipeline structure..."

if ! grep -R "Pipeline" infra/ >/dev/null 2>&1; then
  echo "[WARN] Pipeline reference not found in infra (review recommended)"
fi

############################################
# 7. CHANGE IMPACT CHECK (GIT DIFF GUARD)

echo "[INFO] Checking git diff impact..."

if git diff --cached --name-only | grep -q "^core/"; then
  echo "[INFO] Core changes detected"
fi

if git diff --cached --name-only | grep -q "^infra/.*core"; then
  echo "[FATAL] INFRA TRYING TO TOUCH CORE"
  exit 1
fi

############################################
# 8. CONTEXT FILE CHECK

for f in core_context infra_context pipeline_context; do
  if [ ! -f ".lentra_context/${f}.md" ]; then
    echo "[FATAL] Missing context: $f"
    exit 1
  fi
done

############################################
# 9. FINAL APPROVAL

echo "[OK] FIREWALL PASSED - SAFE TO RUN AIDER"
exit 0
