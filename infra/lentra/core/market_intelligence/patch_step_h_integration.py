from lentra.core.market_intelligence.patch_step_h_pipeline import StepHPatch

def apply_step_h(self, listings):
    return StepHPatch.apply(listings)
