from lentra.bot.state.state_store import StateStore
from lentra.bot.core.state_machine import StateMachine
from lentra.bot.services.ux_state import UXStateAdapter

# AI CONTROL LAYER (soft dependency)
try:
    from lentra.ai_control.telegram_ai_bridge import TelegramAIBridge
    AI_ENABLED = True
    ai_bridge = TelegramAIBridge()
except Exception:
    AI_ENABLED = False
    ai_bridge = None


class InteractionRouter:

    def __init__(self):
        self.store = StateStore()
        self.sm = StateMachine()
        self.ux = UXStateAdapter()

    async def handle(self, user_id: int, action: str, payload: str = None):

        state = self.store.load(user_id)

        # ----------------------------
        # AI CONTROL LAYER HOOK
        # ----------------------------
        if AI_ENABLED and action == "message":
            try:
                ai_result = await ai_bridge.handle_message(
                    user_id=user_id,
                    text=payload or ""
                )

                # AI can override routing
                if ai_result and ai_result.get("override"):
                    self.store.save(state)
                    return ai_result["response"]

                # AI can enrich state
                if ai_result and ai_result.get("state_patch"):
                    patch = ai_result["state_patch"]
                    for k, v in patch.items():
                        setattr(state, k, v)

            except Exception:
                pass  # fallback to legacy flow

        # ----------------------------
        # LEGACY FLOW
        # ----------------------------

        if action == "next":
            state.page += 1

        elif action == "prev":
            state.page = max(0, state.page - 1)

        elif action == "open":
            state = self.sm.set_detail(state, payload)

        elif action == "back":
            state.mode = "LIST"

        self.store.save(state)

        if state.mode == "LIST":
            return self.ux.build_list_view(state)

        if state.mode == "DETAIL":
            return self.ux.build_detail_view(state)

        return "UNKNOWN STATE", None
