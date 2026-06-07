#!/bin/bash
set -e

cd /opt/flyrum

git init || true
git add .
git commit -m "stable checkpoint: worker + postgres queue running"

echo "snapshot done"
