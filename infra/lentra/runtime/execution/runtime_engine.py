import importlib


class RuntimeEngine:
    """
    Execution boundary layer.

    Core НЕ выполняет задачи.
    Runtime — единственный исполнитель.
    """

    def __init__(self):
        self.handlers = {}

    def register(self, task_type: str, handler_path: str):
        """
        handler_path = "module:function"
        """
        module_name, func_name = handler_path.split(":")
        module = importlib.import_module(module_name)
        self.handlers[task_type] = getattr(module, func_name)

    def execute(self, envelope: dict):
        task_type = envelope["type"]

        if task_type not in self.handlers:
            raise Exception(f"No handler for type: {task_type}")

        handler = self.handlers[task_type]
        return handler(envelope)
