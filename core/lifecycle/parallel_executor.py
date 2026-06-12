import threading


class ParallelExecutor:
    """
    Executes workflow steps in parallel where possible.
    """

    def run_parallel(self, steps, handler_map):
        threads = []
        results = []

        def run_step(step):
            fn = handler_map.get(step["type"])
            if fn:
                results.append(fn(step))

        for step in steps:
            t = threading.Thread(target=run_step, args=(step,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return results
