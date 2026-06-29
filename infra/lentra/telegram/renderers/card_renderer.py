class CardRenderer:

    def render_list(self, cards):

        messages = []

        for c in cards:
            msg = f"""
🏠 {c.get('title','')}

💰 {c.get('price')}$
📊 risk: {c.get('risk')}
🧠 verdict: {c.get('verdict')}
📍 {c.get('location')}

confidence: {c.get('confidence')}
"""
            messages.append(msg.strip())

        return messages

    def render_compare(self, cards):

        lines = ["⚖️ Compare results:\n"]

        for c in cards:
            lines.append(f"{c.get('title')} → {c.get('verdict')} ({c.get('price')}$)")

        return "\n".join(lines)
