from abc import ABC, abstractmethod
from lentra.core.market_intelligence.context.engine_context_v3 import EngineContextV3
from lentra.core.market_intelligence.contracts.engine_result_v3 import EngineResultV3


class BaseEngineV3(ABC):

    @abstractmethod
    def evaluate(self, ctx: EngineContextV3) -> EngineResultV3:
        pass
