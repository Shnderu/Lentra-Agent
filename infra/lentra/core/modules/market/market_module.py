from lentra.core.data_layer.builders.task_builder import build_task


class MarketModule:
    def run(self, payload):
        task = build_task(payload)
        query = task.get("query", "")

        objects = [
            {
                "id": "cand-1",
                "price": 575.0,
                "risk": 0.85,
                "area_score": 6.5
            },
            {
                "id": "tg-2",
                "price": 400.0,
                "risk": 0.85,
                "area_score": 6.5
            },
            {
                "id": "fb-3",
                "price": 1200.0,
                "risk": 0.85,
                "area_score": 7.5
            }
        ]

        # КРИТИЧЕСКИ: теперь возвращаем структурированный объект
        return {
            "query": query,
            "snapshot": {
                "objects": objects
            }
        }
