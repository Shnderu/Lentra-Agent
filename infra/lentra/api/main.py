from fastapi import FastAPI
from pydantic import BaseModel

from lentra.services.search_service import SearchService
from lentra.ranking.property_ranker import PropertyRanker
from lentra.responses.search_response import SearchResponseBuilder

app = FastAPI()

search_service = SearchService()


class SearchRequest(BaseModel):
    query: str
    budget: float = 500


@app.post("/search")
async def search(request: SearchRequest):

    properties = await search_service.search(
        request.query
    )

    ranked = PropertyRanker.rank(
        properties,
        request.budget
    )

    return SearchResponseBuilder.build(
        ranked
    )
