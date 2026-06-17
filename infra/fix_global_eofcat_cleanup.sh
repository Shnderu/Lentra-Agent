#!/usr/bin/env bash

set -e

BASE="/opt/lentra/infra/lentra"

echo "[CLEAN] Removing EOFcat injection artifacts..."

# 1. Удаляем ВСЕ строки с EOFcat
find "$BASE" -type f \( -name "*.py" -o -name "*.sql" \) -print0 | while IFS= read -r -d '' file; do
    if grep -q "EOFcat" "$file"; then
        echo "[FIX] cleaning: $file"
        sed -i '/EOFcat/d' "$file"
    fi
done

# 2. Удаляем возможные standalone heredoc leftovers
find "$BASE" -type f -name "*.py" -print0 | while IFS= read -r -d '' file; do
    sed -i '/<< *'\''EOF'\''/d' "$file" || true
done

# 3. Удаляем SQL shell injection lines
find /opt/lentra/infra/migrations -type f -name "*.sql" -print0 | while IFS= read -r -d '' file; do
    sed -i '/cat << '\''EOF'\''/d' "$file" || true
done

echo "[CHECK] Python AST validation..."

python3 - << 'PY'
import compileall
import sys

path = "/opt/lentra/infra/lentra"
ok = compileall.compile_dir(path, force=True, quiet=1)

if not ok:
    print("[ERROR] Python compilation issues detected")
    sys.exit(1)

print("[OK] Python AST clean")
PY

echo "[CHECK] Import graph validation..."

python3 -c "
from lentra.bot.features.rent_search.service import RentSearchService
from lentra.bot.features.rent_search.pipeline.search_pipeline import SearchPipeline
print('[OK] rent_search imports resolved')
"

echo "[DONE] cleanup complete"
