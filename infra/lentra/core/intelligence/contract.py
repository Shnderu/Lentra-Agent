from typing import Protocol, Any, Dict


class IntelligenceEngine(Protocol):
    """
    Канонический контракт AI-слоя Lentra.
    Все реализации (local / remote / advanced graph / external OS) должны его соблюдать.
    """

    def interpret(self, query: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Основной вход:
        - query: пользовательский запрос или системный сигнал
        - context: нормализованный контекст рынка/объектов

        return:
        {
            "result": Any,
            "signals": Dict,
            "confidence": float,
            "meta": Dict
        }
        """
        ...
