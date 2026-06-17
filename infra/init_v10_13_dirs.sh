#!/bin/bash

set -e

mkdir -p lentra/core/system
mkdir -p lentra/services/intelligence
mkdir -p lentra/api
mkdir -p lentra/runtime/bootstrap
mkdir -p lentra/runtime/entrypoint
mkdir -p lentra/runtime/adapters

mkdir -p app/core/control
mkdir -p app/core/graph/runtime_mode

echo "[OK] v10.13 system consolidation directories created"
