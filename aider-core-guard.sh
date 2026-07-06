#!/bin/bash

echo "[GUARD] scanning core duplication risk..."

if find core -type d -name "*_v2" -o -name "*copy*" -o -name "*new*" | grep .; then
  echo "[FATAL] duplicate core modules detected"
  exit 1
fi

echo "[OK] core structure clean"
