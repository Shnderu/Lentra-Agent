#!/bin/bash

set -e

echo "[FIX] replacing stream:rent:tasks → stream:rent:tasks"

FILES=$(grep -R "stream:rent:tasks" -l /opt/lentra/worker)

for f in $FILES; do
  echo "patching $f"
  sed -i 's/stream:rent:tasks/stream:rent:tasks/g' "$f"
done

echo "[DONE]"
