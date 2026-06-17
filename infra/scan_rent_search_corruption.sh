#!/usr/bin/env bash

BASE="/opt/lentra/infra/lentra/bot/features/rent_search"

echo "[SCAN] RENT_SEARCH CORRUPTION CHECK"
echo "BASE: $BASE"
echo ""

echo "=============================="
echo "1. RAW SHELL INJECTION PATTERNS"
echo "=============================="

grep -RIn --include="*.py" "EOFcat" "$BASE" || true
grep -RIn --include="*.py" "<< *EOF" "$BASE" || true
grep -RIn --include="*.py" "cat << " "$BASE" || true
grep -RIn --include="*.py" "bash" "$BASE" || true
grep -RIn --include="*.py" "sh -c" "$BASE" || true
grep -RIn --include="*.py" "rm -rf" "$BASE" || true

echo ""
echo "=============================="
echo "2. PYTHON SYNTAX CHECK"
echo "=============================="

python3 -c "
import os, py_compile

base = '$BASE'
broken = []

for root, _, files in os.walk(base):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            try:
                py_compile.compile(path, doraise=True)
            except Exception as e:
                broken.append((path, str(e)))

if not broken:
    print('[OK] ALL PY FILES VALID')
else:
    print('[BROKEN FILES]')
    for p, e in broken:
        print(p)
        print(' ->', e)
"

echo ""
echo "[DONE]"
