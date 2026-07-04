from lentra.core.market_intelligence.features.feature_governance_v2 import FeatureGovernanceV2


def apply_schema_lock(isolator):
    """
    Hot patch injector for Schema Lock v2
    """

    isolator.schema_lock = FeatureGovernanceV2()

    return isolator
