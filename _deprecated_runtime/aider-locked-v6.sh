#!/bin/bash
set -e

echo "=== LENTRA AIDER LOCKED MODE v6 (STABLE) ==="

REPO="/opt/lentra"
cd "$REPO"

# --- git safety ---
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "[FATAL] Not git repo"
  exit 1
}

BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "[FATAL] main/master blocked"
  exit 1
fi

# --- context safety ---
for f in core_context infra_context pipeline_context; do
  [ ! -f ".lentra_context/${f}.md" ] && {
    echo "[FATAL] Missing context ${f}"
    exit 1
  }
done

# --- ignore safety (no heredoc) ---
if [ ! -f ".aiderignore" ]; then
  printf "%s\n" \
    "venv/" \
    "__pycache__/" \
    "*.pyc" \
    ".git/" \
    "site-packages/" > .aiderignore
fi

# --- limits ---
export AIDER_MAX_CHAT_HISTORY_TOKENS=20000

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

