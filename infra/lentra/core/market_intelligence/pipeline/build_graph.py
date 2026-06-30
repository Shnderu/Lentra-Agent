
from lentra.core.execution.execution_graph import ExecutionGraph

from lentra.core.market_intelligence.steps.dedup_step import DedupStep
from lentra.core.market_intelligence.steps.risk_step import RiskStep


def build_graph(engine):

    return ExecutionGraph([
        DedupStep(engine.dedup),
        RiskStep(engine.risk),
    ])
