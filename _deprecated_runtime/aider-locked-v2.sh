#!/bin/bash
set -euo pipefail

echo "=== LENTRA AIDER LOCKED MODE v2 (SAFE) ==="

REPO="/opt/lentra"
cd "$REPO"

############################################
# 1. GIT SAFETY
############################################

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[FATAL] Not a git repository"
  exit 1
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "[INFO] Branch: $BRANCH"

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "[FATAL] Main branch locked"
  exit 1
fi

############################################
# 2. CONTEXT CHECK
############################################

if [[ ! -f ".lentra_context/core_context.md" ]]; then
  echo "[FATAL] Missing context"
  exit 1
fi

############################################
# 3. IGNORE FILE SAFETY
############################################

if [[ ! -f ".aiderignore" ]]; then
cat <<'IGN' > .aiderignore
venv/
venv-bot/
__pycache__/
*.pyc
*.pyo
*.mat
**/site-packages/
**/.git/
IGN
fi

############################################
# 4. TOKEN SAFETY
############################################

export AIDER_MAX_CHAT_HISTORY_TOKENS=20000

############################################
# 5. RUN AIDER (SEPARATE EXECUTION BLOCK — NO HEREDOC MIX)
############################################

echo "[INFO] Starting Aider locked session"

exec aider \
  --model claude-opus-4-8 \
  --subtree-only \
  --no-auto-commits \
  --no-show-model-warnings \
  --gitignore \
  --read .lentra_context/core_context.md \
  --read .lentra_context/infra_context.md \
  --read .lentra_context/pipeline_context.md
