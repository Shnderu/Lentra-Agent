#!/bin/bash

set -e

echo "===== return { ====="
grep -R -n "return {" \
/opt/lentra/infra/lentra/core/market_intelligence

echo
echo "===== dict( ====="
grep -R -n "dict(" \
/opt/lentra/infra/lentra/core/market_intelligence

echo
echo "===== copy() ====="
grep -R -n "\.copy()" \
/opt/lentra/infra/lentra/core/market_intelligence

echo
echo "===== listing = { ====="
grep -R -n "listing *= *{" \
/opt/lentra/infra/lentra/core/market_intelligence

echo
echo "===== obj = { ====="
grep -R -n "obj *= *{" \
/opt/lentra/infra/lentra/core/market_intelligence

echo
echo "[DONE]"
