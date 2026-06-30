from fastapi import FastAPI
from lentra.core.bootstrap import get_gateway

gateway = get_gateway()

app = FastAPI(title="Lentra Concierge API")


@app.post("/search")
def search(payload: dict):
    """
    Entry API endpoint.
    """
    return gateway.run(payload)
