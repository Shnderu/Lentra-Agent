
class PipelineContext:

    def __init__(self, raw: dict):

        # 🔥 FORCE OBJECT CONTRACT (NO DICT PASS-THROUGH)

        self.raw = raw

        self.title = raw.get("title") or raw.get("q") or ""

        self.search_results = []

        self.snapshot = None

        self.objects = []

        self.enriched_objects = []

        self.market_objects = []

        self.ui = None

        self.risk = None

        self.persona = None
