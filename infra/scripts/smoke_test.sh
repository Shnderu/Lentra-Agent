#!/bin/bash

set -e

echo "[SMOKE TEST] Running pipeline..."

python3 - <<PY
from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine

engine = MarketIntelligenceEngine()

sample = [
    {
        "title": "Nice apartment near beach",
        "price": 700,
        "location": "Da Nang beach",
        "photos": ["x.jpg"]
    },
    {
        "title": "Cheap room urgent",
        "price": 200,
        "location": "Da Nang center",
        "photos": []
    }
]

result = engine.analyze(sample)

print("\nRESULT COUNT:", len(result))

for r in result:
    print({
        "price": r.get("price"),
        "risk": r.get("risk"),
        "confidence": r.get("confidence"),
        "verdict": r.get("verdict")
    })

PY

echo "[DONE]"
