#!/bin/bash

set -e

mkdir -p lentra/core/context
mkdir -p lentra/core/contracts
mkdir -p lentra/core/contracts/pipeline
mkdir -p lentra/core/contracts/rules

mkdir -p lentra/services/pipeline
mkdir -p lentra/services/pipeline/definitions

mkdir -p lentra/runtime/context
mkdir -p lentra/runtime/execution

mkdir -p lentra/domain/pipeline

echo "[OK] v10.16 pipeline + context directories created"
