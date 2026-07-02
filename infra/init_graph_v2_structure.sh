#!/usr/bin/env bash

set -e

BASE="/opt/lentra/infra/lentra/core/market_intelligence/graph_v2"

echo "[GRAPH V2] Creating structure..."

mkdir -p $BASE
mkdir -p $BASE/contracts
mkdir -p $BASE/builder
mkdir -p $BASE/adapters
mkdir -p $BASE/policy

touch $BASE/__init__.py
touch $BASE/contracts/__init__.py
touch $BASE/builder/__init__.py
touch $BASE/adapters/__init__.py
touch $BASE/policy/__init__.py

# core modules
touch $BASE/contracts/graph_contract.py
touch $BASE/builder/graph_builder.py
touch $BASE/adapters/graph_adapter.py
touch $BASE/policy/graph_policy.py

echo "[GRAPH V2] Structure ready"
