from fastapi import APIRouter, Query

from lentra.api.search_handler import SearchHandler

router = APIRouter()

handler = SearchHandler()


@router.get("/search")
def search(q: str = Query(...)):
    """
    Единственный публичный search endpoint.
    """
    return handler.handle(q)
