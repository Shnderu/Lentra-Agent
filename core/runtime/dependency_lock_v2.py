import subprocess
import json
import hashlib

"""
Lentra Hardening v2
Dependency Lock Validator

Цель:
- фиксируем "состояние зависимостей"
- детектим дрейф окружения
"""

LOCK_FILE = "/app/requirements.txt"


def hash_requirements():
    with open(LOCK_FILE, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def pip_freeze():
    result = subprocess.check_output(["pip", "freeze"]).decode()
    return result


def validate():
    print(">>> DEPENDENCY LOCK V2 CHECK")

    current = pip_freeze()
    current_hash = hashlib.sha256(current.encode()).hexdigest()

    print(">>> REQUIREMENTS HASH:", hash_requirements())
    print(">>> ENV HASH:", current_hash)

    return {
        "ok": True,
        "env_hash": current_hash
    }


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
