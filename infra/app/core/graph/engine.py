class GraphEngine:

    def __init__(self, graph):
        self.graph = graph

    def run(self, start_node: str, event, span):

        current = start_node
        ctx = event

        while current:

            node = self.graph.get(current)

            if not node:
                break

            span.start(current)

            result = node.handler(ctx, span)

            span.end(current)

            ctx = result

            current = node.next_node

        return ctx
