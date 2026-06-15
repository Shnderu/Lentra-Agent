from lentra.ml.similarity import cosine_similarity


class RankingService:
    def rank(self, query, properties):
        query_embedding = query.get("query_embedding", [])

        ranked = []

        for p in properties:
            emb = p.get("embedding")

            semantic = cosine_similarity(query_embedding, emb) if emb else 0.0

            tags_score = p.get("score", 0.0)
            rank_score = p.get("rank_score", 0.0)

            final_score = (
                0.5 * semantic +
                0.3 * tags_score +
                0.2 * rank_score
            )

            p["semantic_score"] = semantic
            p["final_score"] = final_score

            ranked.append(p)

        ranked.sort(key=lambda x: x["final_score"], reverse=True)

        return ranked
