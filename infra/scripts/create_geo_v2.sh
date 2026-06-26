#!/bin/bash

set -e

BASE="/opt/lentra/infra/lentra"

echo "[GEO V2] Creating SEA multi-country structure..."

# core geo v2 layer
mkdir -p $BASE/core/geo/v2/router
mkdir -p $BASE/core/geo/v2/countries/vietnam
mkdir -p $BASE/core/geo/v2/countries/thailand
mkdir -p $BASE/core/geo/v2/countries/indonesia
mkdir -p $BASE/core/geo/v2/countries/common

# intelligence layer per country
mkdir -p $BASE/core/intelligence/v2/vietnam
mkdir -p $BASE/core/intelligence/v2/thailand
mkdir -p $BASE/core/intelligence/v2/indonesia

# market segmentation
mkdir -p $BASE/core/market/v2/pricing
mkdir -p $BASE/core/market/v2/risk
mkdir -p $BASE/core/market/v2/ranking

# ingestion routing layer
mkdir -p $BASE/ingestion/v2/router
mkdir -p $BASE/ingestion/v2/connectors/facebook
mkdir -p $BASE/ingestion/v2/connectors/telegram
mkdir -p $BASE/ingestion/v2/connectors/local_sites

# storage segmentation
mkdir -p $BASE/data/v2/raw/vietnam
mkdir -p $BASE/data/v2/raw/thailand
mkdir -p $BASE/data/v2/raw/indonesia

mkdir -p $BASE/data/v2/normalized
mkdir -p $BASE/data/v2/features

echo "[GEO V2] DONE"
