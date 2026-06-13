from lentra.ml.predictor import predict


def rank(properties):
    results = []

    for p in properties:
        score = predict(p)

        results.append({
            "id": p.id,
            "title": p.title,
            "score": score
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
