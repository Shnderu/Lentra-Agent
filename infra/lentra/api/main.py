from fastapi import FastAPI
from pydantic import BaseModel

from lentra.services.pipeline_definition import pipeline

app = FastAPI()


class SearchRequest(BaseModel):
    query: str


@app.post("/search")
def search(req: SearchRequest):

    payload = {
        "query": req.query
    }

    return pipeline.execute(payload)
