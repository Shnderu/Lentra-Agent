from typing import Dict, Any

from lentra.core.market_intelligence.expat.expat_score_engine import (
    ExpatScoreEngine,
)


class PipelineAreaAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Data Layer:
        normalized listing

    Market Intelligence:
        area intelligence

    Output contract:

        area:
            score
            expat_score
            internet_score
            noise_score
            safety_score
            infrastructure_score

    Compatibility:
        keeps flat fields for legacy pipeline consumers.
    """


    def __init__(self):

        self.engine = ExpatScoreEngine()



    def evaluate(
        self,
        item: Dict[str, Any],
    ) -> Dict[str, Any]:


        result = self.engine.evaluate(
            item
        )


        area_score = result.get(
            "area_score",
            0.0
        )


        expat_score = round(
            result.get(
                "expat_score",
                5.0
            )
            /
            10.0,

            2
        )


        internet_score = result.get(
            "internet_score",
            5.0
        )


        noise_score = result.get(
            "noise_score",
            5.0
        )


        safety_score = result.get(
            "safety_score",
            5.0
        )


        infrastructure_score = result.get(
            "infrastructure_score",
            5.0
        )


        area = {

            "score":
                area_score,

            "expat_score":
                expat_score,

            "internet_score":
                internet_score,

            "noise_score":
                noise_score,

            "safety_score":
                safety_score,

            "infrastructure_score":
                infrastructure_score,

        }


        return {

            "area":
                area,


            # compatibility layer

            "area_score":
                area_score,


            "expat_score":
                expat_score,


            "internet_score":
                internet_score,


            "noise_score":
                noise_score,


            "safety_score":
                safety_score,


            "infrastructure_score":
                infrastructure_score,


            "location_context":
                result.get(
                    "location",
                    {}
                ),

        }
