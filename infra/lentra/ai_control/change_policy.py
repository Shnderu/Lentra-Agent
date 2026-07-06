"""
Lentra AI Control Layer - Change Policy
Жёсткие правила для Aider / AI-изменений системы.
"""

class ChangePolicy:
    """
    Политика изменений системы.
    Используется для ограничения Aider и любых AI-агентов.
    """

    # Разрешённые зоны изменений
    ALLOWED_AREAS = {
        "data_layer": True,
        "normalization_layer": True,
        "deduplication_engine": True,
        "market_intelligence": True,
        "risk_scoring": True,
        "ranking": True,
        "bot_handlers": True,
        "parsers": True,
        "utils": True,
    }

    # Запрещённые изменения (архитектурные границы)
    FORBIDDEN_PATTERNS = [
        "new_execution_core",
        "new_ai_engine",
        "parallel_pipeline",
        "graph_runtime_rewrite",
        "second_intelligence_layer",
        "replace_market_intelligence",
    ]

    # Запрещённые файлы/директории
    LOCKED_AREAS = [
        "/infra/lentra/runtime/arch_lock/",
        "/infra/lentra/core/",
    ]

    @staticmethod
    def is_change_allowed(task_text: str) -> bool:
        """
        Примитивная проверка на архитектурную безопасность.
        """
        lowered = task_text.lower()

        for pattern in ChangePolicy.FORBIDDEN_PATTERNS:
            if pattern in lowered:
                return False

        return True

    @staticmethod
    def enforce_prompt(base_prompt: str) -> str:
        """
        Встраивает жёсткие архитектурные ограничения в prompt для Aider.
        """

        policy_block = """
STRICT ARCHITECTURE RULES:

- You are modifying Lentra AI Market Intelligence OS.
- DO NOT create new intelligence cores.
- DO NOT modify execution architecture.
- DO NOT introduce parallel pipelines.
- ONLY improve existing modules.

Allowed:
- parsing improvements
- risk scoring improvements
- deduplication logic
- ranking improvements
- data normalization

Forbidden:
- new system design
- replacing pipeline
- adding competing engines

If unsure → do minimal safe change.
"""

        return policy_block + "\n\n" + base_prompt
