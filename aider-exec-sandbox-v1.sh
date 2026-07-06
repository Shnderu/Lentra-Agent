#!/bin/bash
set -e

echo "=== LENTRA EXECUTION SANDBOX v1 ==="

REPO="/opt/lentra"
cd "$REPO"

############################################
# 1. BASIC GIT SAFETY
############################################

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "[FATAL] Not a git repo"
  exit 1
}

BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "[FATAL] Execution sandbox blocked on main/master"
  exit 1
fi

############################################
# 2. CONTEXT VALIDATION
############################################

for f in core_context infra_context pipeline_context; do
  if [ ! -f ".lentra_context/${f}.md" ]; then
    echo "[FATAL] Missing context: ${f}"
    exit 1
  fi
done

############################################
# 3. CLEAN AIDER FLAGS (CRITICAL FIX)
############################################

AIDER_FLAGS=(
  "--model" "claude-opus-4-8"
  "--subtree-only"
  "--no-auto-commits"
  "--gitignore"
  "--no-show-model-warnings"
  "--read" ".lentra_context/core_context.md"
  "--read" ".lentra_context/infra_context.md"
  "--read" ".lentra_context/pipeline_context.md"
)

############################################
# 4. EXECUTION GATE
############################################

echo "[INFO] Launching controlled Aider runtime..."

exec aider "${AIDER_FLAGS[@]}"
