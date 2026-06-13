from fastapi import FastAPI
from lentra.market.ranker import rank_properties

app = FastAPI()

@app.post("/market/rank")
def rank(data: dict):
    items = data.get("items", [])

    ranked = rank_properties(items)

    return {
        "count": len(ranked),
        "top": ranked[:5]
    }
