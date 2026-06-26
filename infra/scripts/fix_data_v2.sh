#!/bin/bash

set -e

BASE="/opt/lentra/infra/lentra"

echo "[FIX] Creating data v2 module structure..."

mkdir -p $BASE/core/data/v2

# обязательно добавляем __init__.py чтобы Python видел пакет
touch $BASE/core/data/v2/__init__.py

echo "[FIX] DONE"
