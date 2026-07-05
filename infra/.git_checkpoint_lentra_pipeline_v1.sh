#!/bin/bash

set -e

echo "[GIT CHECKPOINT] Lentra AI OS pipeline snapshot"

cd /opt/lentra/infra

git status

git add -A

git commit -m "checkpoint: stable AI OS pipeline v1 (signals/risk/ranking/enrichment working)"

git tag -f stable-pipeline-v1

echo "[OK] checkpoint created: stable-pipeline-v1"

git log -1 --oneline
