#!/bin/bash
set -e

echo "=== LENTRA CONTEXT COMPILER v2 (SEMANTIC + DIFF-AWARE) ==="

REPO="/opt/lentra"
cd "$REPO"

CTX_DIR=".lentra_context"
OUT_DIR="$CTX_DIR/runtime"

mkdir -p "$OUT_DIR"

############################################
# 1. LOAD CANONICAL ARCHITECTURE MODEL
############################################

CORE_MODEL="$OUT_DIR/core_model.txt"

printf "%s\n" \
"core/normalization" \
"core/search" \
"core/ranking" \
"core/risk" \
"core/deduplication" \
"core/market_intelligence" > "$CORE_MODEL"

############################################
# 2. CAPTURE GIT DIFF (INPUT SIGNAL)
############################################

DIFF_FILE="$OUT_DIR/git_diff.txt"

git diff > "$DIFF_FILE" || true

CHANGED_FILES=$(git diff --name-only)

############################################
# 3. BASIC STRUCTURAL DRIFT DETECTION
############################################

echo "[INFO] Checking structural drift..."

echo "$CHANGED_FILES" | grep "^core/" | while read -r f; do
  [ -z "$f" ] && continue

  # forbidden patterns
  echo "$f" | grep -E "v2|v3|new|copy|alt|backup|advisor" >/dev/null 2>&1 && {
    echo "[BLOCK] Forbidden core variant detected: $f"
    exit 1
  }
done

############################################
# 4. SEMANTIC HEURISTIC ANALYSIS
############################################

echo "[INFO] Running semantic heuristics..."

BLOCK_SCORE=0
REVIEW_SCORE=0

# heuristic signals

if echo "$CHANGED_FILES" | grep -q "core/search"; then
  REVIEW_SCORE=$((REVIEW_SCORE+2))
fi

if echo "$CHANGED_FILES" | grep -q "core/normalization"; then
  REVIEW_SCORE=$((REVIEW_SCORE+2))
fi

if echo "$CHANGED_FILES" | grep -q "core/"; then
  REVIEW_SCORE=$((REVIEW_SCORE+1))
fi

# detect expansion of core (new dirs)
NEW_CORE_DIRS=$(git diff --name-only | grep "^core/" | cut -d/ -f2 | sort -u | wc -l)

if [ "$NEW_CORE_DIRS" -gt 6 ]; then
  BLOCK_SCORE=$((BLOCK_SCORE+3))
fi

############################################
# 5. ARCHITECTURE DRIFT CLASSIFICATION
############################################

echo "[INFO] Classifying architecture change..."

if [ "$BLOCK_SCORE" -ge 3 ]; then
  echo "[FATAL] ARCHITECTURE BLOCK (HIGH DRIFT DETECTED)"
  exit 1
fi

if [ "$REVIEW_SCORE" -ge 3 ]; then
  echo "[REVIEW REQUIRED] Potential architecture-sensitive changes detected"
  echo ""
  echo "Changed files:"
  echo "$CHANGED_FILES"
  echo ""
  echo "Manual confirmation required in Decision Gate v2"
fi

############################################
# 6. CONTEXT SNAPSHOT GENERATION
############################################

SNAPSHOT="$OUT_DIR/context_snapshot.md"

printf "%s\n" \
"# LENTRA CONTEXT SNAPSHOT v2" \
"" \
"## Changed Files" \
"$CHANGED_FILES" \
"" \
"## Core Model" \
"$(cat "$CORE_MODEL")" \
"" \
"## Diff Summary" \
"$(git diff --stat)" > "$SNAPSHOT"

############################################
# 7. FINAL OUTPUT CONTRACT
############################################

echo "[OK] Context Compiler v2 completed"
echo "[INFO] Snapshot: $SNAPSHOT"
echo "[INFO] Diff: $DIFF_FILE"
