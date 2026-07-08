class ArchaeologyReporter:


    def build(
        self,
        graph,
        reachable
    ):

        all_files = set(
            graph.nodes.keys()
        )


        dead = all_files - reachable


        return {

            "total_files": len(all_files),

            "reachable": len(reachable),

            "dead_candidates": len(dead),

            "reachable_files": sorted(
                reachable
            ),

            "dead_files": sorted(
                dead
            )

        }
