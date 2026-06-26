#!/bin/bash

set -e

BASE="/opt/lentra/infra/lentra"

echo "[MARKET V2] Creating market intelligence v2 structure..."

# core market intelligence v2
mkdir -p $BASE/core/market/v2/pricing
mkdir -p $BASE/core/market/v2/risk
mkdir -p $BASE/core/market/v2/ranking
mkdir -p $BASE/core/market/v2/segmentation
mkdir -p $BASE/core/market/v2/benchmarks

# country-specific market models
mkdir -p $BASE/core/market/v2/countries/vietnam
mkdir -p $BASE/core/market/v2/countries/thailand
mkdir -p $BASE/core/market/v2/countries/indonesia

# analytics outputs
mkdir -p $BASE/core/market/v2/output/price_analysis
mkdir -p $BASE/core/market/v2/output/risk_reports
mkdir -p $BASE/core/market/v2/output/market_scores

# data feeds for market intelligence
mkdir -p $BASE/data/v2/market/vietnam
mkdir -p $BASE/data/v2/market/thailand
mkdir -p $BASE/data/v2/market/indonesia

echo "[MARKET V2] DONE"
