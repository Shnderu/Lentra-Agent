from lentra.core.bootstrap_env import *

from fastapi import FastAPI
from lentra.core.scenario.bootstrap import bootstrap_scenarios
from lentra.services.pipeline_definition import pipeline

app = FastAPI()


@app.on_event("startup")
def startup():
    bootstrap_scenarios()


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/search")
def search(payload: dict):
    query = payload.get("query", "")

    return pipeline.execute({
        "raw_query": query
    })
