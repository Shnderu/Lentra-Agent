#!/bin/bash

set -e

echo "[SETUP] creating Lentra system directories..."

mkdir -p /opt/lentra/infra/migrations
mkdir -p /opt/lentra/infra/lentra/diag
mkdir -p /opt/lentra/infra/lentra/load
mkdir -p /opt/lentra/infra/lentra/metrics
mkdir -p /opt/lentra/infra/lentra/reports
mkdir -p /opt/lentra/infra/lentra/observability
mkdir -p /opt/lentra/infra/lentra/load/tests

echo "[SETUP] DONE"
