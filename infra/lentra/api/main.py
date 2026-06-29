from fastapi import FastAPI
from pydantic import BaseModel

from lentra.services.pipeline_definition import pipeline

app = FastAPI()


class SearchRequest(BaseModel):
    query: str


@app.post("/search")
def search(req: SearchRequest):
    return pipeline.execute({
        "raw_query": req.query
    })


@app.get("/health")
def health():
    return {"status": "ok"}
