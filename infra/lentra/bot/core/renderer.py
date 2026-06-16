from lentra.telegram.ui.renderer import render_message

class Renderer:
    def render(self, ux: dict) -> str:
        return render_message(ux)


class NullRenderer:
    def render(self, ux: dict) -> str:
        return ""
