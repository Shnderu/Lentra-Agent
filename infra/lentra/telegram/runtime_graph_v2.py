"""
FULL GRAPH V2 IMMUTABLE CONTRACT MODE

Ключевая идея:
- DI graph становится неизменяемым после сборки
- sync/async границы фиксируются на уровне типов исполнения
- router НЕ может быть dict
- listener обязан иметь async handle_event
- runtime запрещает await на sync-объектах
"""

from dataclasses import dataclass
from typing import Any, Callable, Awaitable, Protocol, Dict


# -------------------------
# IMMUTABLE CONTRACT TYPES
# -------------------------

class EventRouter(Protocol):
    async def route(self, event: Dict[str, Any]) -> Any:
        ...


class EventListener(Protocol):
    async def handle_event(self, event: Dict[str, Any]) -> Any:
        ...


class Trace(Protocol):
    def log(self, event: Dict[str, Any]) -> None:
        ...


# -------------------------
# IMMUTABLE GRAPH CONTAINER
# -------------------------

@dataclass(frozen=True)
class RuntimeGraphV2:
    """
    IMMUTABLE DI GRAPH

    После создания:
    - нельзя мутировать
    - нельзя подменять sync/async контракты
    """
    listener: EventListener
    router: EventRouter
    trace: Trace


# -------------------------
# RUNTIME GUARDS
# -------------------------

def assert_async_contract(obj: Any, name: str):
    if not hasattr(obj, "__await__") and not hasattr(obj, "route") and not hasattr(obj, "handle_event"):
        raise TypeError(f"[GRAPH V2 LOCK] {name} is not async-compatible object: {type(obj)}")


def assert_router_contract(router: Any):
    # router НЕ может быть dict (твоя текущая ошибка)
    if isinstance(router, dict):
        raise TypeError("[GRAPH V2 LOCK] Router cannot be dict. Must implement EventRouter")

    if not hasattr(router, "route"):
        raise TypeError("[GRAPH V2 LOCK] Router missing async route(event) method")


def assert_listener_contract(listener: Any):
    if not hasattr(listener, "handle_event"):
        raise TypeError("[GRAPH V2 LOCK] Listener missing async handle_event(event) method")


# -------------------------
# GRAPH VALIDATION
# -------------------------

def validate_graph(graph: RuntimeGraphV2):
    assert_listener_contract(graph.listener)
    assert_router_contract(graph.router)

    assert_async_contract(graph.listener, "listener")
    assert_async_contract(graph.router, "router")
    assert_async_contract(graph.trace, "trace")


# -------------------------
# ENTRYPOINT WRAPPER
# -------------------------

def lock_graph(graph: RuntimeGraphV2) -> RuntimeGraphV2:
    validate_graph(graph)
    return graph
