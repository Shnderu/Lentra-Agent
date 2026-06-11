#!/bin/bash
set -e

echo "[CHECKPOINT] v6.1 ingestion stable"

cd /opt/lentra

git add -A

git commit -m "checkpoint: v6.1 ingestion stable (api+worker+redis flow working)"

git tag stable-v6.1

git push origin stable-v6.1

echo "[CHECKPOINT] done"
