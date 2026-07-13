from lentra.core.contracts.engine_result import EngineResult


class RiskEngineAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Bridges Data Layer risk contract
    with Market Intelligence RiskEngine.

    Data Layer expects:

        risk_score
        risk_level
        signals

    Market Intelligence provides:

        fraud_score
        level
        signals
    """


    def __init__(
        self,
        engine
    ):

        self.engine = engine



    def evaluate(
        self,
        payload: dict,
        market_stats: dict = None,
        duplicate_count: int = 0,
    ) -> dict:


        context = {

            "market_stats":
                market_stats or {},

            "duplicate_count":
                duplicate_count,

        }


        enriched_payload = {

            **payload,

            "_risk_context":
                context,

        }


        result = self.engine.evaluate(
            enriched_payload
        )


        risk = result.get(
            "risk",
            {}
        )


        risk_score = float(
            risk.get(
                "fraud_score",
                0.0
            )
        )


        risk_level = risk.get(
            "level",
            "unknown"
        )


        signals = risk.get(
            "signals",
            []
        )


        engine_result = EngineResult(

            engine_name="market_risk_engine",

            data={

                "risk_score":
                    risk_score,

                "risk_level":
                    risk_level,

                "signals":
                    signals,

                "source":
                    risk.get(
                        "source",
                        "unknown"
                    ),

            },

            trace={

                "adapter":
                    "RiskEngineAdapter",

                "duplicate_count":
                    duplicate_count,

            }

        )


        return {

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "signals":
                signals,

            "engine_result":
                engine_result.__dict__

        }
