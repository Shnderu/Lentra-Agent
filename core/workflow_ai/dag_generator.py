import json

class DAGGenerator:
    """
    Converts task intent → execution graph.
    AI-native orchestration layer (rule-based prototype).
    """

    def build(self, task_type, payload):
        # -----------------------------
        # RENTER DOMAIN LOGIC
        # -----------------------------

        if task_type == "rent.search":
            return {
                "nodes": [
                    {"id": "validate_input"},
                    {"id": "normalize_query"},
                    {"id": "fetch_rentals"},
                    {"id": "rank_results"},
                    {"id": "format_response"}
                ],
                "edges": [
                    ("validate_input", "normalize_query"),
                    ("normalize_query", "fetch_rentals"),
                    ("fetch_rentals", "rank_results"),
                    ("rank_results", "format_response")
                ]
            }

        # fallback generic pipeline
        return {
            "nodes": [
                {"id": "ingest"},
                {"id": "process"},
                {"id": "return"}
            ],
            "edges": [
                ("ingest", "process"),
                ("process", "return")
            ]
        }
