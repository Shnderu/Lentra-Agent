class IntelligencePipelineOrchestrator:

    def __init__(self, engine=None):
        self.engine = engine

    def execute(self, request):
        if not self.engine:
            raise RuntimeError("Engine not injected (bootstrap violation)")

        return self.engine.run(request)


# ================================
# RUNTIME TRACE HOOK (AUDIT LAYER)
# ================================

from lentra.core.runtime_trace_audit import RuntimeTraceAudit

_trace_audit = RuntimeTraceAudit()


def enable_runtime_trace(request_id: str):
    return _trace_audit.start_trace(request_id)


def trace_step(trace, step_name: str, status: str):
    _trace_audit.log_step(trace, step_name, status)


def trace_engine(trace, engine: str, result):
    _trace_audit.log_engine(trace, engine, result)


def trace_failure(trace, error: str):
    _trace_audit.log_failure(trace, error)


def finalize_trace(trace):
    return _trace_audit.finalize(trace)
