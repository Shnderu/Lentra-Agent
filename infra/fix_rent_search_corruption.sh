#!/usr/bin/env bash

set -e

BASE="/opt/lentra/infra/lentra"

echo "[FIX] Removing EOFcat injection patterns..."

# 1. Удаляем все строки с инъекцией
grep -RIl "EOFcat" "$BASE" | while read -r file; do
  echo "[FIX] Cleaning $file"
  sed -i '/EOFcat/d' "$file"
done

echo "[FIX] Removing raw heredoc remnants..."

grep -RIl "cat << 'EOF'" "$BASE" | while read -r file; do
  echo "[FIX] Cleaning heredoc $file"
  sed -i '/cat << '\''EOF'\''/d' "$file"
done

echo "[FIX] Validating Python compilation..."

python3 -m compileall "$BASE" >/dev/null 2>&1 || {
  echo "[ERROR] Python still broken after cleanup"
  exit 1
}

echo "[FIX] Restarting service..."

systemctl restart lentra-bot

echo "[DONE] Corruption fixed and service restarted"
