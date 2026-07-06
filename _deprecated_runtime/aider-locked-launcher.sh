#!/bin/bash
set -e

echo "=== LENTRA AIDER LOCKED MODE ==="

REPO="/opt/lentra"
cd "$REPO"

############################################
# 1. SAFETY CONTEXT LOADING
############################################

export LENTRA_CONTEXT_DIR="$REPO/.lentra_context"

if [ ! -d "$LENTRA_CONTEXT_DIR" ]; then
  echo "[ERROR] Context not found. Run context compiler first."
  exit 1
fi

echo "[OK] Context loaded"

############################################
# 2. AIDER ENV HARD LIMITS
############################################

export AIDER_SUBTREE_ONLY=1
export AIDER_NO_AUTO_COMMITS=0

export OPENAI_API_BASE="https://keys.gridapi.ru/v1"

# ключ НЕ хардкодим в файл (безопасность)
if [ -z "$OPENAI_API_KEY" ]; then
  echo "[ERROR] OPENAI_API_KEY not set"
  exit 1
fi

############################################
# 3. IGNORE HEAVY / NOISE DIRS
############################################

cat > .aiderignore <<'IGN'
venv-bot/
__pycache__/
*.pyc
*.pyo
*.mat
*.so
scipy/
site-packages/
dist/
build/
.git/
IGN

echo "[OK] .aiderignore applied"

############################################
# 4. RUN AIDER IN LOCKED MODE
############################################

aider \
  --model claude-opus-4-8 \
  --subtree-only \
  --no-show-model-warnings \
  --read .lentra_context/core_context.md \
  --read .lentra_context/infra_context.md \
  --read .lentra_context/pipeline_context.md

