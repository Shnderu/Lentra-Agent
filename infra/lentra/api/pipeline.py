from typing import Any, Dict

from lentra.core.observability.replay_engine import ReplayEngine
from lentra.api.pipeline_bootstrap import build_orchestrator


replay_engine = ReplayEngine()
_orchestrator = build_orchestrator()


def run_pipeline(request: Dict[str, Any]) -> Dict[str, Any]:
    try:
        replay_engine.replay(request)
    except Exception:
        pass

    return _orchestrator.execute(request)


def get_pipeline() -> Any:
    return _orchestrator
