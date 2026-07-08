import re
from typing import Dict, Any, Set


class DedupSimilarity:

    """
    Similarity helper for rental objects.

    Purpose:
    - normalize text
    - extract comparable features
    - calculate similarity score
    """


    STOP_WORDS = {
        "studio",
        "apartment",
        "room",
        "near",
        "the",
        "and",
        "with",
        "for"
    }


    def normalize_text(
        self,
        value: str
    ) -> Set[str]:

        if not value:
            return set()


        value = value.lower()


        words = re.findall(
            r"[a-z0-9]+",
            value
        )


        return {
            word
            for word in words
            if word not in self.STOP_WORDS
        }



    def compare(
        self,
        first: Dict[str, Any],
        second: Dict[str, Any]
    ) -> float:


        score = 0.0


        if first.get("city") == second.get("city"):
            score += 0.25


        if first.get("type") == second.get("type"):
            score += 0.15


        first_text = (
            str(first.get("title", ""))
            + " "
            + str(first.get("description", ""))
        )


        second_text = (
            str(second.get("title", ""))
            + " "
            + str(second.get("description", ""))
        )


        first_words = self.normalize_text(
            first_text
        )

        second_words = self.normalize_text(
            second_text
        )


        if first_words and second_words:

            intersection = len(
                first_words &
                second_words
            )

            union = len(
                first_words |
                second_words
            )

            score += (
                intersection /
                max(
                    union,
                    1
                )
            ) * 0.45


        price_one = float(
            first.get(
                "price",
                0
            )
        )

        price_two = float(
            second.get(
                "price",
                0
            )
        )


        if price_one and price_two:

            deviation = abs(
                price_one - price_two
            ) / max(
                price_one,
                price_two
            )


            if deviation <= 0.15:
                score += 0.15


        return round(
            min(score, 1.0),
            3
        )
