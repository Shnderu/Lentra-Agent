from lentra.ml.embedding_service import EmbeddingService


class QueryEmbeddingService:
    def __init__(self):
        self.embedding = EmbeddingService()

    def embed_query(self, query: str):
        if not query:
            return []

        return self.embedding.embed(query)
