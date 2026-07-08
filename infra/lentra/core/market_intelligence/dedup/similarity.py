from typing import Dict, Any


class SimilarityEngine:
    """
    Dedup Intelligence Similarity Engine

    Responsibility:
    - compare normalized listings
    - return similarity score
    """

    def compare(
        self,
        left: Dict[str, Any],
        right: Dict[str, Any]
    ) -> float:

        score = 0.0


        left_title = str(
            left.get(
                "title",
                ""
            )
        ).lower()


        right_title = str(
            right.get(
                "title",
                ""
            )
        ).lower()


        if left_title and right_title:

            left_words = set(
                left_title.split()
            )

            right_words = set(
                right_title.split()
            )

            intersection = len(
                left_words.intersection(
                    right_words
                )
            )

            union = len(
                left_words.union(
                    right_words
                )
            )

            if union:

                score += (
                    intersection /
                    union
                ) * 0.5



        if (
            left.get("city")
            ==
            right.get("city")
        ):

            score += 0.2



        if (
            left.get("type")
            ==
            right.get("type")
        ):

            score += 0.1



        left_price = float(
            left.get(
                "price",
                0
            )
        )


        right_price = float(
            right.get(
                "price",
                0
            )
        )


        if left_price and right_price:

            diff = abs(
                left_price -
                right_price
            ) / max(
                left_price,
                right_price
            )

            if diff < 0.1:

                score += 0.2


        return round(
            min(
                score,
                1.0
            ),
            3
        )
