from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Protocol, runtime_checkable


# =========================
# IMMUTABLE CORE CONTRACTS
# =========================

@runtime_checkable
class AsyncEventListenerContract(Protocol):
    async def handle_event(self, event: dict) -> dict: ...


@runtime_checkable
class AsyncRouterContract(Protocol):
    async def route(self, event: dict) -> dict: ...


@dataclass(frozen=True)
class GraphV2:
    """
    IMMUTABLE DI GRAPH V2

    После создания:
    - нельзя менять зависимости
    - нельзя подменять runtime компоненты
    """

    listener: AsyncEventListenerContract
    router: AsyncRouterContract
    trace: Any = None

    def validate(self) -> None:
        # hard contract enforcement at boot time
        if not isinstance(self.listener, AsyncEventListenerContract):
            raise TypeError("listener must implement AsyncEventListenerContract")

        if not isinstance(self.router, AsyncRouterContract):
            raise TypeError("router must implement AsyncRouterContract")


class GraphV2Lock:
    """
    HARD LOCK LAYER:
    запрещает runtime mutation DI graph
    """

    def __init__(self, graph: GraphV2):
        graph.validate()
        self._graph = graph

    @property
    def graph(self) -> GraphV2:
        return self._graph


