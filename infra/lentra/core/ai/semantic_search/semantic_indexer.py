

from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed
from lentra.core.ai.semantic_search.vector_store.vector_store import add_listing


def index_listing(listing):

    text = f"{listing['title']} {listing.get('location','')} {listing.get('city','')}"

    vector = embed(text)

    add_listing(listing, vector)
