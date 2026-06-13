from lentra.ml.predictor import predict


def rank(properties, vector_scores=None):
    results = []

    for p in properties:

        ml_score = predict(p)

        vector_score = 0
        if vector_scores and p.id in vector_scores:
            vector_score = 1 / (1 + vector_scores[p.id])

        final = (ml_score * 0.7) + (vector_score * 0.3)

        results.append({
            "id": p.id,
            "title": p.title,
            "score": final
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
