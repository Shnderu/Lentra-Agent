#!/bin/bash
set -e

echo "=== LENTRA AIDER PREFLIGHT v5 (NO HEREDOC SAFE MODE) ==="

REPO="/opt/lentra"
cd "$REPO"

############################################
# GIT SAFETY
############################################

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "[FATAL] Not a git repo"
  exit 1
}

BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "[INFO] Branch: $BRANCH"

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "[FATAL] main/master blocked"
  exit 1
fi

############################################
# CONTEXT SAFETY
############################################

if [ ! -f ".lentra_context/core_context.md" ]; then
  echo "[FATAL] Missing core context"
  exit 1
fi

############################################
# SAFE .AIDERIGNORE (NO HEREDOC)
############################################

if [ ! -f ".aiderignore" ]; then
  printf "%s\n" \
    "venv/" \
    "__pycache__/" \
    "*.pyc" \
    "*.pyo" \
    ".git/" \
    "site-packages/" > .aiderignore
fi

############################################
# LIMITS
############################################

export AIDER_MAX_CHAT_HISTORY_TOKENS=20000

############################################
# RUN AIDER
############################################

echo "[INFO] Starting Aider..."

exec aider \
  --model claude-opus-4-8 \
  --subtree-only \
  --no-auto-commits \
  --no-show-model-warnings \
  --gitignore \
  --read .lentra_context/core_context.md \
  --read .lentra_context/infra_context.md \
  --read .lentra_context/pipeline_context.md

