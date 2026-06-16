class Container:
    """
    DI container без зависимости на UI слой.

    Принцип:
    - bot-core НЕ импортирует telegram/ui вообще
    - UI подключается на уровне handlers
    """

    def __init__(self):
        pass
