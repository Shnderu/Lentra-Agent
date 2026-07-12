# Legacy `rent_search` Migration

> Documentation only. This file authorizes no deletion and no code change.
> Subordinate to `infra/ARCHITECTURE_CONSTITUTION.md`; deletion authority is
> `infra/ARCHITECTURE_DELETION_MANIFEST.md` (Batch B §3.9); baseline evidence
> is `infra/ARCH_LOCK_PHASE3_SOAK_REPORT.md` (frozen 2026-07-12: 84 violations,
> 0 on spine, SPINE CLEAN).
>
> Paths are relative to `/opt/lentra`.

---

## 1. Current legacy subtree

`infra/lentra/bot/features/rent_search/` — a self-contained legacy feature
contour inside the production bot package, predating the canonical flow. It
carries its own copies of responsibilities the Constitution assigns to the
canonical spine:

| Subtree area | What it contains | Duplicated canonical responsibility |
|---|---|---|
| `pipeline/` (`search_pipeline.py`, `provider_factory.py`) | own search pipeline + provider wiring | `api/pipeline/search_pipeline.py` (SearchPipeline) |
| `providers/` (`base/`, `sea/` thailand/vietnam, `scraper/`, `social/`, `mock_provider`) | own multi-source provider layer | ingestion/normalization upstream of the canonical pipeline |
| `application/` (`aggregator/rent_aggregator`, `use_cases/query_parser`, `dto/search_context`, `services/normalizer`) | own aggregation/normalization | SearchAdapter + ListingContractGuard boundary |
| `ranking/` (`ranking_service`) | own ranking | `UnifiedRankingEngine` (the ONLY ranking authority, Constitution §6.5) |
| `contract/`, `contracts/` (`rent_item`, request/response) | own data contracts | canonical listing contracts |
| `service`, `feature`, `handler`, `repository`, `mapper`, `data/` | own feature service/handler/persistence glue | canonical bot → API HTTP path |

Status in the arch_lock dry-run baseline: **~45 of the 69
`LEGACY_INTELLIGENCE_ISOLATION` hits are edges internal to this tree**
(legacy-to-legacy). They vanish wholesale when the tree is deleted — the
expected single large counter drop of Batch B (SOAK report §3.4 note 2).

The tree also imports two external legacy targets (both themselves legacy,
outside the production graph):

- `lentra.rent.connectors.scraper_connector` (from `providers/scraper/`, `providers/sea/vietnam_provider`)
- `lentra.rent.runtime.observability.*` (metrics, trace_recorder — from `service`)

## 2. External production consumers

Exactly **two** modules of the production bot package import into the tree
(baseline edge list, SOAK report §1.2; recorded as Grandfathered Baseline
rows 10–11 in the Deletion Manifest §8):

| Consumer | Import edge | Rule hit |
|---|---|---|
| `infra/lentra/bot/handlers/rent_handler.py` | → `bot.features.rent_search.handler` | `LEGACY_INTELLIGENCE_ISOLATION` |
| `infra/lentra/bot/handlers/router_builder.py` | → `bot.features.rent_search.service` | `LEGACY_INTELLIGENCE_ISOLATION` |

The production bot path (`bot/main.py`, `bot/handlers/handlers.py`,
`bot/cards/intelligence_renderer.py` — DO-NOT-TOUCH list) does **not** depend
on the tree. The two consumers above are side handlers; removing their import
lines is a code edit inside the production bot package and is therefore a
separate, later step — **not** part of any deletion batch.

## 3. Migration target architecture

The Constitution (§2–§3) allows exactly one runtime flow. Everything the
legacy tree does is already served by the canonical spine:

```
Bot (thin delivery, aiogram)
  -> HTTP call to API /search            # the bot imports NO pipeline / intelligence code
API: lentra.api.main -> api/routes/search.py
  -> api/pipeline/__init__.py (singleton)
  -> SearchPipeline (api/pipeline/search_pipeline.py)
      -> SearchAdapter -> ListingContractGuard -> MarketService
      -> GatewayV3 -> AreaEngine / MarketIntelligenceEngine / RiskEngine / DedupEngine
      -> UnifiedRankingEngine -> DecisionLayer -> ObjectIntelligenceCardBuilder
```

Target state for rent search: the bot's rent-search UX (if the product keeps
it) is a thin handler that calls the API `/search` endpoint and renders the
returned intelligence cards. No provider logic, no aggregation, no ranking,
no contracts inside the bot.

## 4. Replacement mapping

| Legacy module (in tree) | Canonical replacement | Notes |
|---|---|---|
| `pipeline/search_pipeline.py` | `api/pipeline/search_pipeline.py` (via HTTP `/search`) | bot never imports the pipeline directly |
| `pipeline/provider_factory.py`, `providers/*` | canonical ingestion upstream of the pipeline | provider/source logic is not a bot concern |
| `application/aggregator/rent_aggregator.py` | `SearchAdapter` + `DedupEngine` | aggregation + collapsing on the spine |
| `application/services/normalizer.py`, `dto/search_context.py` | `ListingContractGuard` + canonical request contract | boundary contract enforcement |
| `application/use_cases/query_parser.py` | API request schema (`api/routes/search.py`) | parsing at the delivery boundary |
| `ranking/ranking_service.py` | `UnifiedRankingEngine` | ranking pluralism is forbidden (Constitution §11.4) |
| `contracts/rent_item.py`, `contract/request|response` | canonical listing/response contracts | one contract set |
| `service`, `feature`, `repository`, `data/*` | API-backed handler; persistence via canonical repositories | no feature-local persistence |
| `handler` | thin `bot/handlers/*` handler calling API `/search` | replaces the two consumer imports in §2 |

No new components are required: every row maps onto an existing canonical
module. This migration adds nothing to the architecture.

## 5. Deletion conditions

The tree is deleted as **Deletion Manifest Batch B §3.9**, subject to all of:

1. **Manifest preconditions met** (Manifest §7): documents committed,
   enforcement step done — batches run in order A → B, one batch per commit,
   rollback git tag before the batch.
2. **Fresh grep at deletion time** confirms the only remaining external
   importers are the two §2 consumers (Grandfathered rows 10–11) — any new
   importer is a regression to revert first (SOAK invariant INV-D).
3. **Consumer decision recorded**: either (a) the rent-search UX is retired
   and `rent_handler.py` / `router_builder.py` import lines are removed in a
   separate, later code change, or (b) those handlers are re-pointed to the
   API `/search` path — in both cases *outside* the deletion batch. Until
   then rows 10–11 stay grandfathered; note they become ImportError-latent
   once the tree is gone (Manifest §8 note), so the consumer decision should
   land in the same release window.
4. **Post-deletion verification** (SOAK checklist C1–C3):
   - runner exit = 0, rules loaded = 11, SPINE CLEAN;
   - violation counter drops to the expected post-Batch-B value **28**
     (= 17 Batch-C edges + 11 grandfathered); any edge not in Batch C or
     Manifest §8 is a regression;
   - `lentra-api`, `lentra-bot`, `lentra-recovery` active after restart +
     `/health` check.
5. **Archival, not silent deletion** where the batch protocol requires it;
   the rollback point (git tag) is mandatory before the batch.

Nothing in this document changes rules, SEAL, arch_lock, or code.
