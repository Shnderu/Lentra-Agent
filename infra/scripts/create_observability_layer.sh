#!/bin/bash

BASE="/opt/lentra/infra/lentra/rent/runtime/observability"

mkdir -p $BASE
mkdir -p $BASE/tracer
mkdir -p $BASE/metrics
mkdir -p $BASE/replay

echo "[OK] observability layer created"
