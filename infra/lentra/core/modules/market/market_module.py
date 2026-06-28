from lentra.core.data_layer.builders.task_builder import build_task


class MarketModule:
    def run(self, payload: dict):

        # 🔒 НОРМАЛИЗАЦИЯ ВХОДА
        if isinstance(payload, str):
            payload = {"title": payload}

        task = build_task(payload)

        query = task.get("query", payload.get("title", ""))

        # TEMP dataset (v3 stable)
        objects = [
            {
                "id": "cand-1",
                "price": 575.0,
                "risk": 0.85,
                "area_score": 6.5,
                "final_score": 0.5,
                "verdict": "neutral"
            },
            {
                "id": "tg-2",
                "price": 400.0,
                "risk": 0.85,
                "area_score": 6.5,
                "final_score": 0.5,
                "verdict": "neutral"
            },
            {
                "id": "fb-3",
                "price": 1200.0,
                "risk": 0.85,
                "area_score": 7.5,
                "final_score": 0.5,
                "verdict": "neutral"
            }
        ]

        return {
            "query": query,
            "objects": objects,
            "total": len(objects),
            "average_price": sum(o["price"] for o in objects) / len(objects)
        }
