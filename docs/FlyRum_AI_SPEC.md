# FlyRum AI — Canonical Product Specification

## ⚠️ RULE OF TRUTH
This file is the SINGLE source of truth for product architecture.
Any code that conflicts with this spec is considered invalid.

---

## 🎯 Mission
FlyRum AI — Telegram travel assistant that identifies opportunities, not tickets.

---

## 🏗 Architecture
Telegram Bot → Intent Router → PostgreSQL Queue → Workers → Services → Providers

---

## 🔀 Intent Scenarios (ONLY VALID TYPES)
1. route_search
2. watch_route
3. budget_search
4. deal_search
5. ai_planner
6. error_fare

---

## ⚙️ Core Rules
- Every request MUST go through Intent Router
- All async work MUST go through PostgreSQL Queue
- Workers are stateless
- No direct external API calls from bot layer

---

## 🚫 Forbidden
- bypassing queue
- direct worker invocation
- hardcoded workflows outside router
