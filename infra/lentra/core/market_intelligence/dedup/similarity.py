from typing import Dict, Any


class SimilarityEngine:
    """
    Dedup Intelligence Similarity Engine V5

    Responsibility:
    - compare normalized listings
    - use property context
    - detect same property across sources
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

            union = len(
                left_words.union(
                    right_words
                )
            )

            if union:

                score += (
                    len(
                        left_words.intersection(
                            right_words
                        )
                    )
                    /
                    union
                ) * 0.25



        if (
            left.get("city")
            and
            left.get("city")
            ==
            right.get("city")
        ):

            score += 0.15



        if (
            left.get("segment_key")
            and
            left.get("segment_key")
            ==
            right.get("segment_key")
        ):

            score += 0.35



        left_location = left.get(
            "location",
            {}
        )

        right_location = right.get(
            "location",
            {}
        )


        if isinstance(
            left_location,
            dict
        ) and isinstance(
            right_location,
            dict
        ):

            if (
                left_location.get("district")
                and
                left_location.get("district")
                ==
                right_location.get("district")
            ):

                score += 0.15



        if (
            left.get("type")
            ==
            right.get("type")
        ):

            score += 0.05



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

            if diff < 0.15:

                score += 0.05



        return round(
            min(
                score,
                1.0
            ),
            3
        )
