# FIX: JSON serialization safe analyzer v1

import json

def safe(obj):
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, dict):
        return {k: safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [safe(x) for x in obj]
    return obj


def main():
    result = build_arch_graph()  # твоя текущая логика

    # CRITICAL FIX: normalize sets before json dump
    result = safe(result)

    print(json.dumps(result, indent=2))


def build_arch_graph():
    # placeholder — твоя текущая реализация
    return {
        "nodes": set(["api", "runtime", "intelligence"]),
        "edges": set([
            ("api", "runtime"),
            ("runtime", "arch_lock")
        ])
    }


if __name__ == "__main__":
    main()
