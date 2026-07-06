#!/bin/bash
set -e

echo "[LENTRA CHECKPOINT] starting..."

cd /opt/lentra

git status

git add -A

git commit -m "checkpoint: graph_v2 stabilized as routing layer + selector/router working"

git log -1

echo "[LENTRA CHECKPOINT] done"
