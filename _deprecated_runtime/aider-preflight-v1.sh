#!/bin/bash
set -e

echo "=== LENTRA AIDER PREFLIGHT v1 (NO-HEREDOC SAFE MODE) ==="

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
# 2. CONTEXT CHECK
############################################

test -f .lentra_context/core_context.md || {
  echo "[FATAL] Missing core context"
  exit 1
}

test -f .lentra_context/infra_context.md || {
  echo "[FATAL] Missing infra context"
  exit 1
}

test -f .lentra_context/pipeline_context.md || {
  echo "[FATAL] Missing pipeline context"
  exit 1
}

############################################
# 3. AIDER CHECK
############################################

command -v aider >/dev/null 2>&1 || {
  echo "[FATAL] aider not installed"
  exit 1
}

############################################
# 4. .AIDERIGNORE SAFE WRITE (NO HEREDOC)
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
# 5. SAFETY LIMITS
############################################

export AIDER_MAX_CHAT_HISTORY_TOKENS=20000

############################################
# 6. RUN AIDER (CLEAN EXEC)
############################################

echo "[INFO] Starting Aider..."

exec aider \
  --model claude-opus-4-8 \
  --subtree-only \
  --no-auto-commits \
  --gitignore \
  --read .lentra_context/core_context.md \
  --read .lentra_context/infra_context.md \
  --read .lentra_context/pipeline_context.md
