

from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed
from lentra.core.ai.semantic_search.vector_store.vector_store import add_listing


class IngestionEngine:

    def ingest(self, raw_listing: dict):

        listing = {
            "id": raw_listing["id"],
            "title": raw_listing.get("title", ""),
            "price": raw_listing.get("price", 0),
            "city": raw_listing.get("city", ""),
            "location": raw_listing.get("location", ""),
            "source": raw_listing.get("source", "unknown")
        }

        vector = embed(listing["title"])

        add_listing(listing, vector)

        print(f"[INGEST] stored {listing['id']}")

        return listing
