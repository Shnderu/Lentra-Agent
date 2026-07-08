from collections import deque


class ReachabilityAnalyzer:


    def analyze(
        self,
        graph,
        entrypoints
    ):

        visited = set()

        queue = deque(
            entrypoints
        )


        while queue:

            current = queue.popleft()


            if current in visited:

                continue


            visited.add(
                current
            )


            node = graph.nodes.get(
                current
            )


            if not node:

                continue


            for dependency in node.imports:

                queue.append(
                    dependency
                )


        return visited
