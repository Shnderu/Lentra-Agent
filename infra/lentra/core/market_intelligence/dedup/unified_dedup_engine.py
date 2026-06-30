from typing import Dict, Any


class UnifiedDedupEngine:
    """
    Contract-compliant dedup engine
    """

    def __init__(self):
        pass

    def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        title = item.get("title", "")
        price = item.get("price", 0)

        signature = f"{title.lower()}::{price}"

        item["dedup_signature"] = signature
        item["is_duplicate"] = False

        return item
