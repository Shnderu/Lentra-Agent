#!/usr/bin/env bash

set -e

BASE="/opt/lentra/infra/lentra"

echo "[FIX] Step 1 - detecting corrupted files..."

FILES=$(grep -RIl "EOFcat" "$BASE" || true)

if [ -z "$FILES" ]; then
  echo "[OK] No corrupted files found"
else
  echo "[FIX] Removing corrupted modules:"
  echo "$FILES"

  for f in $FILES; do
    echo "[REMOVE] $f"
    rm -f "$f"
  done
fi

echo "[FIX] Step 2 - removing SQL contamination"

SQL_FILES=$(grep -RIl "EOFcat" /opt/lentra/infra/migrations || true)

for f in $SQL_FILES; do
  echo "[REMOVE SQL] $f"
  rm -f "$f"
done

echo "[FIX] Step 3 - restoring from git (if available)"

if git -C /opt/lentra/infra rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C /opt/lentra/infra checkout -- lentra || true
  git -C /opt/lentra/infra checkout -- migrations || true
fi

echo "[FIX] Step 4 - python compilation check"

python3 -m compileall "$BASE"

echo "[FIX] Step 5 - restarting service"

systemctl restart lentra-bot

echo "[DONE] FULL RESTORE COMPLETED"
