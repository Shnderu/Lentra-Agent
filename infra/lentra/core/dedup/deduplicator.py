from typing import List, Dict, Any
import hashlib


def _hash_item(item: Dict[str, Any]) -> str:
    """
    Простой стабильный ключ дедупликации.
    Сейчас: цена + локация + заголовок (если есть)
    """
    base = f"{item.get('title','')}_{item.get('price','')}_{item.get('location','')}"
    return hashlib.md5(base.encode("utf-8")).hexdigest()


def deduplicate(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Базовый dedup engine (MVP уровень).
    Группирует одинаковые объявления по хэшу.
    """
    seen = {}
    result = []

    for item in items:
        key = _hash_item(item)

        if key in seen:
            # добавляем ссылку на дубль
            seen[key]["duplicates"].append(item)
        else:
            item["duplicates"] = []
            seen[key] = item
            result.append(item)

    return result
