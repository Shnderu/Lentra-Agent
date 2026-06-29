from lentra.scenarios.registry import scenario_registry

# ⚠️ forced registration side-effects
import lentra.scenarios.rent_scenario_v1  # noqa: F401
import lentra.scenarios.pricing_scenario_v1  # noqa: F401
import lentra.scenarios.default_scenario_v1  # noqa: F401

__all__ = ["scenario_registry"]
