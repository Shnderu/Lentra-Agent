from lentra.property.models import Property


class PropertyRanker:

    @staticmethod
    def rank(properties: list[Property], budget: float):

        ranked = []

        for p in properties:

            score = p.trust_score

            if p.price <= budget:
                score += 50

            ranked.append(
                {
                    "property": p,
                    "score": score
                }
            )

        ranked.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked
