# ============================================================
# DEPRECATED REPOSITORY LAYER (DISABLED)
# ============================================================
# Ранее: property_core upsert layer
# Сейчас: исключён из системы
# ============================================================

class PropertyRepository:
    """
    DISABLED REPOSITORY
    """

    def __init__(self, conn):
        self.conn = conn

    def upsert(self, p):
        # no-op
        return None
