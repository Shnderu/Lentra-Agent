#!/bin/bash
set -e

echo "=== LENTRA ARCHITECTURE DECISION GATE v1 ==="

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
  echo "[FATAL] MAIN BRANCH BLOCKED"
  exit 1
fi

############################################
# 2. BASELINE CORE CONTRACT
############################################

ALLOWED_CORE="normalization search ranking risk deduplication market_intelligence"

############################################
# 3. DETECT CORE MODULES
############################################

echo "[INFO] Scanning core modules..."

for d in core/*; do
  [ -d "$d" ] || continue

  name=$(basename "$d")

  echo "$ALLOWED_CORE" | grep -qw "$name"
  if [ $? -ne 0 ]; then

    echo ""
    echo "=============================="
    echo "[ARCHITECTURE DECISION REQUIRED]"
    echo "New core module detected: core/$name"
    echo "=============================="
    echo ""
    echo "Choose action:"
    echo "  1) MERGE into existing core module"
    echo "  2) PROMOTE to new approved domain"
    echo "  3) REJECT / DELETE"
    echo ""

    printf "Enter choice [1-3]: "
    read CHOICE

    if [ "$CHOICE" = "1" ]; then
      echo "[OK] You chose MERGE (manual refactor required)"
    elif [ "$CHOICE" = "2" ]; then
      echo "[WARN] PROMOTE selected"
      echo "IMPORTANT: You MUST update:"
      echo " - context compiler"
      echo " - firewall allowlist"
      echo " - architecture contract"
    else
      echo "[ACTION] REJECT selected"
      echo "Deleting core/$name"
      rm -rf "core/$name"
    fi

  fi
done

############################################
# 4. DUPLICATE PATTERN CHECK
############################################

echo "[INFO] Checking duplicate patterns..."

if find core -type d | grep -E "_v[0-9]+|_new|_copy|_alt|backup|duplicate" >/dev/null 2>&1; then
  echo "[FATAL] DUPLICATE ARCHITECTURE VARIANTS DETECTED"
  find core -type d | grep -E "_v[0-9]+|_new|_copy|_alt|backup|duplicate"
  exit 1
fi

############################################
# 5. INFRA LEAK CHECK
############################################

echo "[INFO] Checking infra leakage..."

if grep -R "core/" infra/ >/dev/null 2>&1; then
  echo "[FATAL] INFRA IS DIRECTLY ACCESSING CORE"
  exit 1
fi

if grep -R "ranking\|risk\|normalization\|search" infra/ >/dev/null 2>&1; then
  echo "[FATAL] BUSINESS LOGIC DETECTED IN INFRA"
  exit 1
fi

############################################
# 6. CONTEXT CHECK
############################################

for f in core_context infra_context pipeline_context; do
  if [ ! -f ".lentra_context/${f}.md" ]; then
    echo "[FATAL] Missing context file: $f"
    exit 1
  fi
done

############################################
# 7. FINAL OK

echo "[OK] ARCHITECTURE GATE PASSED"
exit 0
