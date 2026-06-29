from fastapi import FastAPI
from pydantic import BaseModel

from lentra.core.scenario.bootstrap import bootstrap_scenarios

# Обязательно загружаем все сценарии ДО создания pipeline
bootstrap_scenarios()

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
