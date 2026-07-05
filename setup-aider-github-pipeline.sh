#!/bin/bash
set -e

echo "=== Lentra Aider → GitHub Autopipeline Setup ==="

cd /opt/lentra

echo "[1] Git status"
git status || true

echo "[2] Create Aider config"

cat <<'YAML' > /opt/lentra/.aider.conf.yml
model: openai/claude-opus-4-8
auto-commits: true
dirty-commits: false
subtree-only: true
gitignore: true
model-warnings: false
read:
  - core/
  - infra/
  - services/
YAML

echo "[3] Setup git hooks"

mkdir -p /opt/lentra/.git/hooks

cat <<'HOOK' > /opt/lentra/.git/hooks/pre-push
#!/bin/bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
  echo "BLOCKED: push to main"
  exit 1
fi
HOOK

chmod +x /opt/lentra/.git/hooks/pre-push

cat <<'HOOK' > /opt/lentra/.git/hooks/post-commit
#!/bin/bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)

if [[ "$BRANCH" == feature/aider-* ]]; then
  git push origin "$BRANCH"
fi
HOOK

chmod +x /opt/lentra/.git/hooks/post-commit

echo "[DONE] Aider GitHub pipeline installed"
