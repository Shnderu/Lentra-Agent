class Container:
    """
    Core DI container.

    ВАЖНО:
    - НЕ импортируем UI на уровне модуля
    - исключаем circular dependency bot-core ↔ telegram-ui
    """

    def __init__(self):
        self._renderer = None

    @property
    def renderer(self):
        # lazy import, чтобы не ловить import cycle при старте
        if self._renderer is None:
            from lentra.telegram.ui.renderer import Renderer
            self._renderer = Renderer()
        return self._renderer
