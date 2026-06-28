
from lentra.core.ai.concierge.ui.view_model_mapper import ViewModelMapper


class UIModule:

    def __init__(self):

        self.engine = ViewModelMapper()

    def run(self, ctx):

        # SAFETY: only MarketObject allowed
        if not hasattr(ctx, "market_objects"):

            ctx.ui = []

            return ctx

        ctx.ui = [
            self.engine.build_card(obj)
            for obj in ctx.market_objects
        ]

        return ctx
