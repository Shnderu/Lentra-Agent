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
            "market_stats": market_stats or {},
            "duplicate_count": duplicate_count,
        }


        result = self.engine.evaluate(
            payload,
            context
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


        return {

            "risk_score": risk_score,

            "risk_level": risk_level,

            "signals": signals,


            "engine_result": EngineResult(

                score=risk_score,

                deviation=risk.get(
                    "deviation",
                    0.0
                ),

                signal=risk_level,

                raw=risk,

            ).to_dict()

        }
