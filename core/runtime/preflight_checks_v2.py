import redis
import time
import importlib

"""
Lentra Hardening v2
Preflight system check
"""

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

REQUIRED_MODULES = [
    "redis",
    "aiogram",
    "httpx",
    "psycopg2"
]


def check_imports():
    missing = []

    for m in REQUIRED_MODULES:
        try:
            importlib.import_module(m)
        except Exception:
            missing.append(m)

    return missing


def check_redis():
    try:
        return r.ping()
    except Exception as e:
        return str(e)


def run():
    print(">>> PREFLIGHT V2 START")

    result = {
        "ts": time.time(),
        "imports_missing": check_imports(),
        "redis": check_redis()
    }

    print(result)

    if result["imports_missing"]:
        raise RuntimeError(f"Missing deps: {result['imports_missing']}")

    if result["redis"] != True:
        raise RuntimeError("Redis unavailable")

    print(">>> PREFLIGHT PASSED")
    return True


if __name__ == "__main__":
    run()
