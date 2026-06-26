from app.intent.router import IntentRouter
from app.core.scenario.scenario_engine_v1 import ScenarioEngineV1


def init_gateway():
    """
    FIX: гарантируем корректную инициализацию dependency graph
    """
    scenario_engine = ScenarioEngineV1()

    # FIX: router теперь без registry/ctx ошибок
    intent_router = IntentRouter()

    return intent_router, scenario_engine
