#!/bin/bash
set -e

echo "=== LENTRA AIDER PREFLIGHT VALIDATOR v1 (HARD SAFE) ==="

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
# 2. CONTEXT CHECK
############################################

for f in core_context infra_context pipeline_context; do
  if [ ! -f ".lentra_context/${f}.md" ]; then
    echo "[FATAL] Missing .lentra_context/${f}.md"
    exit 1
  fi
done

############################################
# 3. AIDER CHECK
############################################

command -v aider >/dev/null 2>&1 || {
  echo "[FATAL] aider not installed"
  exit 1
}

############################################
# 4. IGNORE FILE SAFETY (NO HEREDOC)
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
# 5. TOKEN LIMIT SAFETY
############################################

export AIDER_MAX_CHAT_HISTORY_TOKENS=20000

############################################
# 6. RUN AIDER (LOCKED MODE)

echo "[INFO] Starting Aider..."

exec aider \
  --model claude-opus-4-8 \
  --subtree-only \
  --no-auto-commits \
  --gitignore \
  --read .lentra_context/core_context.md \
  --read .lentra_context/infra_context.md \
  --read .lentra_context/pipeline_context.md
