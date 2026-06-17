#!/usr/bin/env bash

echo "[IMPORT CHECK] rent_search critical imports"
echo ""

python3 - << 'PY'
import importlib

modules = [
    "lentra.bot.features.rent_search.service",
    "lentra.bot.features.rent_search.pipeline.search_pipeline",
    "lentra.bot.features.rent_search.providers.sea.sea_provider",
    "lentra.bot.features.rent_search.contracts",
    "lentra.bot.features.rent_search.mapper",
]

broken = []

for m in modules:
    try:
        importlib.import_module(m)
        print("[OK]", m)
    except Exception as e:
        print("[FAIL]", m, "->", e)
        broken.append(m)

print("\nRESULT:", "CLEAN" if not broken else "BROKEN IMPORT GRAPH")
PY

echo ""
echo "[DONE]"
