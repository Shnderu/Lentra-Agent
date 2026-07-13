from typing import Dict, Any

from lentra.core.engines.base_engine import BaseEngine


class AreaEngine(BaseEngine):
    """
    Canonical Market Intelligence Area Engine.

    Contract:
    input:
        context dict

    output:
        normalized area intelligence dict

    Responsibility:
    - detect city context
    - provide area confidence score
    """


    def run(
        self,
        ctx: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = ctx.get(
            "query",
            ""
        )

        city = ctx.get(
            "city"
        )


        if city:

            detected = city


        elif "da nang" in query.lower():

            detected = "da_nang"


        else:

            detected = "unknown"



        return {

            "score": 0.5,

            "city": detected,

            "country":
                "Vietnam"
                if detected == "da_nang"
                else "unknown",

            "area": {

                "detected": detected,

                "status": "ok"

            },

            "version": "area_v3_canonical"

        }
