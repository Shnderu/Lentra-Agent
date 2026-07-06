#!/bin/bash
set -e

echo "=== LENTRA RUNTIME v1 CONSOLIDATION ==="

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

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "[FATAL] Runtime blocked on main/master"
  exit 1
fi

echo "[INFO] Branch: $BRANCH"

############################################
# 2. CONTEXT REQUIREMENT
############################################

CTX_DIR=".lentra_context"

for f in core_context.md infra_context.md pipeline_context.md; do
  if [ ! -f "$CTX_DIR/$f" ]; then
    echo "[FATAL] Missing context: $f"
    exit 1
  fi
done

############################################
# 3. LEGACY RUNTIME DETECTION (NO DELETION)
############################################

echo "[INFO] Checking legacy runtime scripts..."

ls /opt/lentra | grep -E "aider-preflight|aider-locked|setup-aider" || true

############################################
# 4. LOAD CONFIG (OPTIONAL)
############################################

CONFIG_ARGS=()

if [ -f ".aider.conf.yml" ]; then
  CONFIG_ARGS+=("-c" ".aider.conf.yml")
fi

############################################
# 5. EXECUTION
############################################

echo "[INFO] Launching unified Aider runtime..."

exec aider \
  --model claude-opus-4-8 \
  --subtree-only \
  --no-auto-commits \
  --gitignore \
  --no-show-model-warnings \
  --read .lentra_context/core_context.md \
  --read .lentra_context/infra_context.md \
  --read .lentra_context/pipeline_context.md \
  "${CONFIG_ARGS[@]}"
