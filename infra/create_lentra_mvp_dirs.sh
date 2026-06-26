#!/bin/bash

set -e

BASE="/opt/lentra/infra/lentra/core"

mkdir -p $BASE/pipeline

mkdir -p $BASE/parsing
mkdir -p $BASE/data
mkdir -p $BASE/normalization
mkdir -p $BASE/dedup
mkdir -p $BASE/market
mkdir -p $BASE/risk
mkdir -p $BASE/ranking
mkdir -p $BASE/response

mkdir -p /opt/lentra/infra/lentra/worker

echo "Lentra MVP pipeline directories created"
