

from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed
from lentra.core.ai.semantic_search.vector_store.vector_store import add_listing


def index_listing(listing: dict):

    vec = embed(listing.get("title", ""))

    add_listing(listing, vec)
