from typing import Any, Dict, Callable, List
import time


class RuntimeTrace:
    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []

    def node(self, name: str, data: Dict[str, Any] = None):
        node_id = f"{name}:{time.time_ns()}"
        self.nodes.append({
            "id": node_id,
            "name": name,
            "data": data or {}
        })
        return node_id

    def edge(self, src: str, dst: str, meta: Dict[str, Any] = None):
        self.edges.append({
            "from": src,
            "to": dst,
            "meta": meta or {}
        })

    def dump(self):
        print("\n===== RUNTIME GRAPH (FULL TRACE) =====")
        for e in self.edges:
            print(f"{e['from']} -> {e['to']} :: {e['meta']}")
        print("\n===== NODES =====")
        for n in self.nodes:
            print(n)
        print("=======================================\n")


def traced(name: str, trace: RuntimeTrace):
    def wrapper(fn: Callable):
        def inner(*args, **kwargs):
            node_id = trace.node(name, {
                "args": str(args)[:200],
                "kwargs": str(kwargs)[:200],
            })

            result = fn(*args, **kwargs)

            if hasattr(result, "__trace_id__"):
                trace.edge(node_id, result.__trace_id__)
            else:
                trace.node(f"{name}:result", {
                    "type": str(type(result)).__name__
                })

            return result
        return inner
    return wrapper
