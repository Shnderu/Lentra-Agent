# Lentra Architecture Consolidation Map V1

Дата: 2026-07-10

Назначение:
Фиксация целевой архитектуры Lentra как SEA Rent Intelligence / AI Property OS.

Главный принцип:

Lentra не является агрегатором объявлений.
Lentra является AI Market Intelligence слоем над рынком аренды.

Ценность:
- анализ реальной цены рынка
- поиск дублей
- риск-анализ
- анализ районов
- AI-объяснение выбора


==================================================
1. TARGET ARCHITECTURE
==================================================

DATA SOURCES

    |
    v

INGESTION LAYER

    |
    v

PROPERTY NORMALIZATION

    |
    v

MARKET OBJECT MODEL

    |
    v

==================================================
MARKET INTELLIGENCE CORE
==================================================

    |
    +--> Pricing Intelligence
    |
    +--> Dedup Intelligence
    |
    +--> Risk Intelligence
    |
    +--> Area Intelligence
    |
    +--> Ranking Intelligence
    |
    +--> Market History
    |
    +--> Decision Layer

    |
    v

AI DECISION LAYER

    |
    v

OBJECT INTELLIGENCE CARD

    |
    v

Telegram Mini App / API / UI


==================================================
2. APPROVED CORE
==================================================


## Market Intelligence

KEEP:

lentra/core/market_intelligence/


Это главный интеллект системы.


--------------------------------------------------
Pricing Intelligence
--------------------------------------------------

KEEP:

lentra/core/market_intelligence/pricing/


Ответственность:

- рыночная цена
- сравнение цены объекта с рынком
- переплата / выгода
- история изменения цены


Главные компоненты:

market_truth_engine.py
market_service.py



--------------------------------------------------
Dedup Intelligence
--------------------------------------------------

KEEP:

lentra/core/market_intelligence/dedup/


Ответственность:

- поиск одинаковых объектов
- группировка дублей
- определение источника


Главные компоненты:

dedup_index.py
entity_resolver.py
unified_dedup_engine.py


Это один из ключевых активов Lentra.



--------------------------------------------------
Risk Intelligence
--------------------------------------------------

TARGET:

lentra/core/market_intelligence/risk/


Основной движок:

risk_engine_v2.py


Временно оставить:

risk_adapter.py
risk_engine_adapter.py


Причина:

совместимость со старым runtime.



--------------------------------------------------
Ranking Intelligence
--------------------------------------------------

TARGET:

lentra/core/market_intelligence/ranking/


Основной движок:

unified_ranking_engine.py


Все остальные ranking системы являются кандидатами на консолидацию.



--------------------------------------------------
Area Intelligence
--------------------------------------------------

KEEP:

lentra/core/market_intelligence/area/


Ответственность:

Expat Area Score:

- интернет
- шум
- безопасность
- инфраструктура
- экспат-среда


Основные компоненты:

area_engine.py
micro_market_engine.py
temporal_market_engine.py



--------------------------------------------------
Decision Layer
--------------------------------------------------

KEEP:

lentra/core/market_intelligence/decision/


Ответственность:

Создание AI-вердикта.


Пример:

"Цена выше рынка на 11%, но район имеет высокий expat score и низкий риск."



Основные компоненты:

ai_decision_engine.py
market_decision_core.py
decision_layer.py



--------------------------------------------------
Output Layer
--------------------------------------------------

KEEP:

lentra/core/market_intelligence/output/


Ответственность:

Формирование пользовательского ответа.


Основные компоненты:

facade.py
object_intelligence_card.py
assembler.py



==================================================
3. PIPELINE AND RUNTIME
==================================================

KEEP:

lentra/core/pipeline/


Главные точки:

canonical_search_pipeline.py
runtime.py
worker_search_entrypoint.py


Назначение:

Оркестрация выполнения.


Важно:

Pipeline НЕ является интеллектом.

Он только вызывает Market Intelligence Core.



==================================================
4. API AND INTERFACE
==================================================

KEEP:

lentra/api/


Главные точки:

api/search_handler.py
api/pipeline/search_pipeline.py


Назначение:

API слой между пользователем и интеллектом.



==================================================
5. TELEGRAM
==================================================

KEEP:

lentra/telegram/


Правило:

Telegram только интерфейс.

Бизнес-логика аренды должна находиться в:

lentra/core/market_intelligence/



==================================================
6. ADAPTER LAYER
==================================================

Оставить временно:

lentra/services/


Задача:

превратить сервисы в тонкие адаптеры.


Пример:

Было:

services/ranking_service.py

    |
    v

собственный ranking


Должно быть:

services/ranking_service.py

    |
    v

Market Intelligence Ranking



==================================================
7. LEGACY CANDIDATES
==================================================


НЕ удалять сейчас.


Только пометить.


Кандидаты:


## Старые ranking системы


lentra/core/ranking/

lentra/domain/ranking/

lentra/rent/ranking/

app/core/ranking/


Причина:

дублирование Ranking Intelligence.



## Старый rent слой


lentra/rent/


Причина:

старая модель:

"агрегатор объявлений"


Новая модель:

"AI аналитический слой рынка"



## Старые intelligence слои


services/intelligence.py

services/intelligence_orchestrator.py

core/intelligence/



==================================================
8. ARCHITECTURE RULES
==================================================


Запрещено:


telegram

api

services

rent

domain


создавать собственные:

- pricing
- ranking
- risk
- dedup
- market analysis



Разрешено только:


UI

 |

API

 |

MARKET INTELLIGENCE CORE

 |

DATA



==================================================
9. NEXT STEPS
==================================================


После фиксации карты:


1. Создать import dependency map.

2. Классифицировать модули:

KEEP
ADAPTER
LEGACY


3. Убрать дубли только после проверки зависимостей.


4. После каждого крупного блока:

- rebuild
- tests
- git checkpoint



END
