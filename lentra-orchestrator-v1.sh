#!/bin/bash
set -e

echo "=== LENTRA RUNTIME ORCHESTRATOR v1 ==="

REPO="/opt/lentra"
cd "$REPO"

############################################
# 1. GIT SAFETY LAYER
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
# 2. CORE ARCHITECTURE LOCK
############################################

for d in core/normalization core/search core/ranking core/risk core/deduplication core/market_intelligence
do
  if [ ! -d "$d" ]; then
    echo "[FATAL] Missing core module: $d"
    exit 1
  fi
done

############################################
# 3. CONTEXT CONTRACT CHECK
############################################

CTX_DIR=".lentra_context"

[ -f "$CTX_DIR/core_context.md" ] || { echo "[FATAL] missing core_context"; exit 1; }
[ -f "$CTX_DIR/infra_context.md" ] || { echo "[FATAL] missing infra_context"; exit 1; }
[ -f "$CTX_DIR/pipeline_context.md" ] || { echo "[FATAL] missing pipeline_context"; exit 1; }

############################################
# 4. CORE DRIFT DETECTOR (lightweight)
############################################

echo "[INFO] Checking forbidden core mutations..."

if find core -maxdepth 1 -type d | grep -E "v2|new|copy|alt|backup" >/dev/null 2>&1; then
  echo "[FATAL] FORBIDDEN CORE VARIANT DETECTED"
  exit 1
fi

if find core -type d -name "*advisor*" >/dev/null 2>&1; then
  echo "[FATAL] FORBIDDEN MODULE: advisor"
  exit 1
fi

############################################
# 5. AIDER VALIDATION
############################################

command -v aider >/dev/null 2>&1 || {
  echo "[FATAL] aider not installed"
  exit 1
}

############################################
# 6. IGNORE POLICY (NO HEREDOC)
############################################

if [ ! -f ".aiderignore" ]; then
  printf "%s\n%s\n%s\n%s\n%s\n" \
    "venv/" \
    "__pycache__/" \
    "*.pyc" \
    "*.pyo" \
    ".git/" \
    "site-packages/" > .aiderignore
fi

############################################
# 7. CONTEXT LOADING STRATEGY
############################################

CORE_CTX="$CTX_DIR/core_context.md"
INFRA_CTX="$CTX_DIR/infra_context.md"
PIPE_CTX="$CTX_DIR/pipeline_context.md"

############################################
# 8. TOKEN SAFETY
############################################

export AIDER_MAX_CHAT_HISTORY_TOKENS=20000

############################################
# 9. EXECUTION LAYER
############################################

echo "[INFO] Starting Aider (ORCHESTRATED MODE)..."

exec aider \
  --model claude-opus-4-8 \
  --subtree-only \
  --no-auto-commits \
  --gitignore \
  --read "$CORE_CTX" \
  --read "$INFRA_CTX" \
  --read "$PIPE_CTX"
