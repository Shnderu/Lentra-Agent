#!/bin/bash
set -e

# CORE LAYERS (CANONICAL)

mkdir -p /opt/lentra/infra/lentra/core/intent
mkdir -p /opt/lentra/infra/lentra/core/scenario
mkdir -p /opt/lentra/infra/lentra/core/gateway
mkdir -p /opt/lentra/infra/lentra/core/contracts
mkdir -p /opt/lentra/infra/lentra/core/adapters
mkdir -p /opt/lentra/infra/lentra/core/normalizers

# EXECUTION / DI GRAPH
mkdir -p /opt/lentra/infra/lentra/core/graph
mkdir -p /opt/lentra/infra/lentra/core/graph/engine
mkdir -p /opt/lentra/infra/lentra/core/graph/nodes
mkdir -p /opt/lentra/infra/lentra/core/graph/contracts

# WORKER LAYER
mkdir -p /opt/lentra/infra/lentra/worker

# OBSERVABILITY
mkdir -p /opt/lentra/infra/lentra/core/observability
mkdir -p /opt/lentra/infra/lentra/core/observability/alerts

# UX LAYER
mkdir -p /opt/lentra/infra/lentra/core/ux

# SESSION / MEMORY
mkdir -p /opt/lentra/infra/lentra/core/session
mkdir -p /opt/lentra/infra/lentra/core/memory
mkdir -p /opt/lentra/infra/lentra/core/context

echo "[OK] Lentra core directory structure initialized"
