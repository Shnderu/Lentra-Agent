from typing import Any, Dict, List


class CanonicalSearchEntrypoint:
    """
    ЕДИНАЯ ТОЧКА ВХОДА В ПОИСКОВЫЙ PIPELINE (v3).

    Запрещает:
    - обход pipeline
    - прямой доступ к dedup/ranking/market logic из API

    Все запросы обязаны проходить через этот слой.
    """

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def execute(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Единственный разрешённый путь обработки search results.
        """

        if not objects:
            return []

        # HARD BOUNDARY: никакой логики вне pipeline
        return self.pipeline.run(objects)
