# ============================================================
# DEPRECATED LAYER (DISABLED)
# ============================================================
# Ранее: PropertyIngestionService → property_core
# Сейчас: выключено из активного pipeline
# ============================================================

class PropertyIngestionService:
    """
    DISABLED SERVICE
    Не участвует в runtime pipeline.

    Active data source:
    - public.properties (via vietnam_provider)
    """

    def __init__(self, conn):
        self.conn = conn

    def ingest(self, raw: dict, source_type: str):
        # no-op: ingestion disabled
        return None
# ============================================================
# DEPRECATED LAYER (DISABLED)
# ============================================================
# Ранее: PropertyIngestionService → property_core
# Сейчас: выключено из активного pipeline
# ============================================================

class PropertyIngestionService:
    """
    DISABLED SERVICE
    Не участвует в runtime pipeline.

    Active data source:
    - public.properties (via vietnam_provider)
    """

    def __init__(self, conn):
        self.conn = conn

    def ingest(self, raw: dict, source_type: str):
        # no-op: ingestion disabled
        return None
