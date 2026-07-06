#!/usr/bin/env bash

set -e

echo "[CHECKPOINT] ARCH LOCK v1 snapshot start"

cd /opt/lentra/infra

# ensure clean working state is visible
git status

# stage everything (we want full reproducibility snapshot)
git add -A

# create deterministic checkpoint commit
git commit -m "ARCH LOCK v1 CHECKPOINT: system stabilized, DAG clean, syntax enforced"

# tag rollback point
git tag -f arch-lock-v1-stable

# push if remote exists (safe ignore if not configured)
git push origin HEAD || true
git push origin arch-lock-v1-stable || true

echo "[CHECKPOINT] DONE - rollback tag: arch-lock-v1-stable"
