#!/bin/bash

set -e

mkdir -p lentra/core/graph/compiler
mkdir -p lentra/core/graph/runtime
mkdir -p lentra/core/graph/contracts

mkdir -p lentra/core/compiler
mkdir -p lentra/core/compiler/validation
mkdir -p lentra/core/compiler/analysis

mkdir -p lentra/runtime/compiler

mkdir -p lentra/services/pipeline
mkdir -p lentra/services/pipeline/builders

mkdir -p lentra/domain/pipeline/graph

echo "[OK] v10.18 architecture compiler directories created"
