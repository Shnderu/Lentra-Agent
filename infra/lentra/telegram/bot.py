from lentra.telegram.router.intent_router import IntentRouter
from lentra.telegram.handlers.search_handler import SearchHandler
from lentra.telegram.renderers.card_renderer import CardRenderer

class LentraBot:

    def __init__(self, engine):
        self.engine = engine
        self.router = IntentRouter()
        self.search_handler = SearchHandler(engine)
        self.renderer = CardRenderer()

    def handle(self, update: dict):

        text = update.get("text", "")

        intent = self.router.detect(text)

        if intent == "search":
            results = self.search_handler.handle(text)
            return self.renderer.render_list(results)

        if intent == "compare":
            results = self.search_handler.handle(text)
            return self.renderer.render_compare(results)

        if intent == "explain":
            return self.renderer.render_explanation(text)

        return "Unsupported query"
