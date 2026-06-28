from fastapi import FastAPI, Query
from lentra.core.pipeline.pipeline import LentraPipeline

app = FastAPI(title="Lentra Concierge API")

pipeline = LentraPipeline()


@app.get("/search")
def search(q: str = Query(...)):
    ctx = pipeline.run({"title": q})

    snapshot = getattr(ctx, "snapshot", None)

    objects = []
    total = 0
    average_price = 0.0

    if snapshot and hasattr(snapshot, "objects"):
        objects = snapshot.objects
        total = len(objects)
        average_price = (
            sum(o.get("price", 0) for o in objects) / total
            if total > 0 else 0.0
        )

    return {
        "query": q,
        "total": total,
        "average_price": average_price,
        "objects": objects,
    }


@app.get("/debug")
def debug(q: str = Query("test")):
    ctx = pipeline.run({"title": q})

    return {
        "ok": True,
        "type": str(type(ctx)),
        "has_snapshot": hasattr(ctx, "snapshot"),
        "ctx": repr(ctx),
    }
