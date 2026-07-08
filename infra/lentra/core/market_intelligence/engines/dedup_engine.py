from typing import Dict, Any, List
import hashlib
import re


class DedupEngine:
    """
    V3 DEDUP CONTRACT

    Responsibility:
    - create object fingerprint
    - normalize listing identity
    - estimate duplicate similarity

    Current stage:
    - local similarity contract
    - no persistent external index
    """

    def evaluate(
        self,
        result: Dict[str, Any],
        candidates: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}

        fingerprint = self.build_fingerprint(
            result
        )

        duplicates = []
        confidence = 0.0

        if candidates:

            for candidate in candidates:

                if not isinstance(candidate, dict):
                    continue

                if candidate.get("id") == result.get("id"):
                    continue

                score = self.similarity_score(
                    result,
                    candidate
                )

                if score >= 0.75:
                    duplicates.append(
                        candidate
                    )

                    confidence = max(
                        confidence,
                        score
                    )


        sources = list(
            {
                item.get(
                    "source",
                    "unknown"
                )
                for item in duplicates
                if item.get("source")
            }
        )


        canonical_listing = None

        if duplicates:

            canonical_listing = min(
                [
                    result
                ] + duplicates,
                key=lambda x: str(
                    x.get(
                        "id",
                        ""
                    )
                )
            ).get(
                "id"
            )


        result["dedup"] = {

            "duplicates": len(
                duplicates
            ),

            "confidence": round(
                confidence,
                2
            ),

            "sources": sources,

            "canonical_listing": canonical_listing,

            "fingerprint": fingerprint,

            "status": "similarity_checked"

        }


        return result


    def similarity_score(
        self,
        left: Dict[str, Any],
        right: Dict[str, Any]
    ) -> float:

        score = 0.0


        if self.normalize_text(
            left.get(
                "title",
                ""
            )
        ) == self.normalize_text(
            right.get(
                "title",
                ""
            )
        ):
            score += 0.45


        if str(
            left.get(
                "city",
                ""
            )
        ).lower() == str(
            right.get(
                "city",
                ""
            )
        ).lower():

            score += 0.2


        if str(
            left.get(
                "type",
                ""
            )
        ).lower() == str(
            right.get(
                "type",
                ""
            )
        ).lower():

            score += 0.15


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

            delta = abs(
                left_price - right_price
            ) / max(
                left_price,
                right_price
            )

            if delta <= 0.05:
                score += 0.2


        return min(
            score,
            1.0
        )


    def normalize_text(
        self,
        value: Any
    ) -> str:

        text = str(
            value or ""
        ).lower()

        text = re.sub(
            r"[^a-z0-9 ]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()


    def build_fingerprint(
        self,
        result: Dict[str, Any]
    ) -> str:

        city = str(
            result.get(
                "city",
                ""
            )
        ).lower()


        property_type = str(
            result.get(
                "type",
                "apartment"
            )
        ).lower()


        title = self.normalize_text(
            result.get(
                "title",
                ""
            )
        )


        raw = "|".join(
            [
                city,
                property_type,
                title,
            ]
        )


        return hashlib.sha256(
            raw.encode(
                "utf-8"
            )
        ).hexdigest()[:16]
