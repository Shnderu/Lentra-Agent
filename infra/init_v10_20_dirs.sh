#!/bin/bash

set -e

mkdir -p lentra/core/compiler/types
mkdir -p lentra/core/compiler/semantic
mkdir -p lentra/core/compiler/compatibility
mkdir -p lentra/core/compiler/diff

mkdir -p lentra/core/typesystem
mkdir -p lentra/core/typesystem/layers
mkdir -p lentra/core/typesystem/contracts
mkdir -p lentra/core/typesystem/validation

mkdir -p lentra/core/graph/types
mkdir -p lentra/core/graph/semantic

mkdir -p lentra/runtime/types

mkdir -p lentra/services/types

mkdir -p lentra/domain/types

echo "[OK] v10.20 architecture type system directories created"
