Expand ARCHITECTURE_CONSTITUTION.md and CANONICAL_COMPONENT_MAP.md.

Documentation only.

Do not modify Python files.
Do not create new architecture.
Do not change project structure.

The documents must establish:

Product identity:

Lentra = AI Market Intelligence OS for SEA rental market.

Canonical runtime flow:

SearchPipeline
 -> SearchAdapter
 -> ListingContractGuard
 -> MarketService
 -> GatewayV3
 -> AreaEngine
 -> MarketIntelligenceEngine
 -> RiskEngine
 -> DedupEngine
 -> UnifiedRankingEngine
 -> DecisionLayer
 -> ObjectIntelligenceCardBuilder


Ownership rules:

MarketService owns market truth.

UnifiedRankingEngine owns ranking.

DecisionLayer owns final decision.

RiskEngine has veto authority.


Legacy isolation:

Any duplicate pipeline, ranking engine, intelligence engine,
decision engine or alternative orchestration path is legacy.

Legacy modules must not receive new imports.


Architecture governance:

Any architectural change requires ADR.

Add verification rules for automated architecture checker.

The documents must become production-grade architecture
documentation and the single source of truth.

