
from fastapi import FastAPI, Query
from lentra.core.pipeline.pipeline import LentraPipeline

app = FastAPI()

pipeline = LentraPipeline()


@app.get("/search")
def search(q: str = Query(...)):

    try:

        ctx = pipeline.run({"title": q})

    except Exception as e:

        return {"error": str(e)}

    s = ctx.snapshot

    return {
        "query": s.query,
        "total": s.total_objects,
        "average_price": s.average_market_price,
        "objects": [
            {
                "id": o.id,
                "price": o.market_price,
                "risk": o.risk,
                "area_score": o.area_score,
                "verdict": o.verdict,
                "negotiation": o.negotiation,
            }
            for o in s.objects
        ]
    }
