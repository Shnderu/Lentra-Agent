#!/bin/bash

set -e

mkdir -p lentra/core/guards
mkdir -p lentra/runtime/bootstrap
mkdir -p lentra/core/contracts
mkdir -p lentra/core/contracts/dto
mkdir -p lentra/core/contracts/enforcement
mkdir -p lentra/services
mkdir -p lentra/services/policies
mkdir -p lentra/domain/policies
mkdir -p lentra/data/policies

mkdir -p app/core/guards

echo "[OK] v10.15 enforcement directories created"
