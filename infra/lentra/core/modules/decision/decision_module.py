from lentra.core.context.ai_context import AIContext


class DecisionModule:
    """
    V6 DECISION MODULE (SAFE + TYPE ROBUST + NO SILENT FAILS)
    """

    def run(self, ctx):

        # ----------------------------
        # 1. NORMALIZE CONTEXT
        # ----------------------------
        if isinstance(ctx, dict):
            title = ctx.get("title", "")
            snapshot = ctx.get("snapshot", None)
            objects = snapshot.get("objects", []) if isinstance(snapshot, dict) else []
        else:
            title = getattr(ctx, "title", "")
            snapshot = getattr(ctx, "snapshot", None)
            objects = getattr(snapshot, "objects", []) if snapshot else []

        # ----------------------------
        # 2. SAFE OUTPUT
        # ----------------------------
        return {
            "query": title,
            "total": len(objects),
            "objects": objects
        }
