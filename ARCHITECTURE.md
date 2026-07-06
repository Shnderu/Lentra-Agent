# Lentra Architecture Lock File (v1)

This document defines the canonical architecture of the Lentra system.
It is the single source of truth for all AI-assisted development (Aider, LLM tools, agents).

Any change that violates this document is INVALID unless explicitly approved.

---

# 1. CORE SYSTEM DEFINITION

Lentra is a SINGLE Market Intelligence OS for SEA rental market.

It is NOT:
- a generic backend framework
- a graph execution engine platform
- a multi-registry system
- a workflow orchestration framework

It is:

> Market Intelligence Interpretation System

---

# 2. CANONICAL ARCHITECTURE (ONLY VALID MODEL)

## 2.1 Execution Layer (STRICT)

EngineRegistry:
- ONLY execution engines
- stateless business logic units
- NO intelligence decisions

Allowed engines:
- pricing
- risk
- dedup
- area
- signals
- expat

Rules:
- MUST NOT contain "market_intelligence"
- MUST NOT contain orchestration logic
- MUST NOT decide fallback behavior

---

## 2.2 Intelligence Layer (SINGLE CORE)

MarketIntelligenceEngine:
- SINGLE source of intelligence logic
- fallback for all unknown requests
- interprets market context
- aggregates signals from engines

Rules:
- MUST NOT be split into sub-engines
- MUST NOT be duplicated into V2/V3 variants
- MUST remain single class concept

---

## 2.3 API Layer

pipeline.py:
- thin request entry point
- no business logic
- no decision trees
- only orchestration delegation

Orchestrator:
- routes request to EngineRegistry OR MarketIntelligenceEngine
- MUST NOT introduce additional abstraction layers

---

# 3. FORBIDDEN ARCHITECTURAL ACTIONS

The following are STRICTLY FORBIDDEN:

## 3.1 Engine duplication
- EngineRegistryV2
- EngineRegistryV3
- any alternative registry implementations

## 3.2 Graph / workflow systems
- graph-based execution engines as core architecture
- DAG execution systems replacing registry

## 3.3 Intelligence fragmentation
- splitting MarketIntelligenceEngine into sub-engines
- creating "AI layers" above MI engine

## 3.4 Parallel orchestration systems
- introducing second orchestrator
- creating "pipeline frameworks"

---

# 4. Fallback RULE (CRITICAL)

If request type is unknown:

✔ MUST use:
MarketIntelligenceEngine

✘ MUST NOT:
- invent new engine types
- fallback to registry keys like "market_intelligence"
- extend registry for fallback purposes

---

# 5. SINGLE SOURCE OF TRUTH RULE

There must be ONLY ONE:
- EngineRegistry
- MarketIntelligenceEngine
- Orchestrator

Any additional versioned duplicates are considered architectural regression.

---

# 6. AI / AIDER RULES

All AI-assisted code generation MUST:

- follow this file strictly
- refuse to introduce new architecture layers
- prioritize minimal patch fixes
- never perform "refactor for cleanliness" unless explicitly requested

If instruction conflicts with this file → THIS FILE WINS.

---

# 7. CHANGE POLICY

Allowed:
- bug fixes
- minimal safety improvements
- small refactors inside existing class boundaries

Not allowed:
- redesign architecture
- splitting modules into new systems
- introducing abstractions not already present

---

# 8. SYSTEM PRINCIPLE

> Value is in market interpretation, not infrastructure complexity.

Lentra = Market Intelligence Layer over fragmented SEA rental data.

NOT a platform for building platforms.
