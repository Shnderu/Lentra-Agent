from lentra.db.session import SessionLocal
from lentra.domain.property.search import search_properties


class SearchService:

    def __init__(self, api_url: str | None = None):
        self.api_url = api_url

    async def search(self, query: str):

        db = SessionLocal()

        try:

            payload = {
                "text": query,
                "city": "Da Nang"
            }

            results = search_properties(
                payload=payload,
                conn=db
            )

            return results

        finally:
            db.close()
