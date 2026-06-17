#!/bin/bash

set -e

mkdir -p lentra/core/seal
mkdir -p lentra/core/guards
mkdir -p lentra/core/contracts
mkdir -p lentra/core/contracts/pipeline
mkdir -p lentra/core/contracts/pipeline_lock

mkdir -p lentra/core/guards/side_effects

mkdir -p lentra/domain/_internal
mkdir -p lentra/domain/_seal

mkdir -p lentra/services/pipeline
mkdir -p lentra/services/pipeline/definitions

mkdir -p lentra/runtime/seal

echo "[OK] v10.17 system sealing directories created"
