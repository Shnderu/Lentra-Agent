from typing import Callable, Any


class HandlerTraceWrapper:

    def __init__(self, trace):
        self.trace = trace

    def wrap(self, handler_name: str, fn: Callable):

        def wrapped(*args, **kwargs):

            trace_id = None

            if self.trace:
                trace_id = self.trace.emit(
                    "handler",
                    "enter",
                    {
                        "handler": handler_name,
                        "args": str(args)[:200]
                    }
                )

            try:
                result = fn(*args, **kwargs)

                if self.trace:
                    self.trace.emit(
                        "handler",
                        "exit",
                        {
                            "handler": handler_name,
                            "result_type": type(result).__name__
                        }
                    )

                return result

            except Exception as e:

                if self.trace:
                    self.trace.emit(
                        "handler",
                        "error",
                        {
                            "handler": handler_name,
                            "error": str(e)
                        }
                    )

                raise

        return wrapped
