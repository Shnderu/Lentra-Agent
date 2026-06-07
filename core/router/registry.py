HANDLERS = {}


def register(task_type: str):
    def wrapper(func):
        HANDLERS[task_type] = func
        return func
    return wrapper
