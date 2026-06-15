from fastapi import FastAPI, Depends
from lentra.db.deps import get_db
from lentra.services.search_service import SearchService
from lentra.domain.models.search import SearchRequest, SearchResponse, PropertyDTO

app = FastAPI()


@app.post("/v1/search", response_model=SearchResponse)
def search(payload: SearchRequest, db=Depends(get_db)):
    service = SearchService(db)

    results = service.search(
        raw_query=payload.query,
        budget_max=payload.budget_max,
    )

    return SearchResponse(
        query=payload.query,
        results=[PropertyDTO(**r) for r in results]
    )
