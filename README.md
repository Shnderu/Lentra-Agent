# FlyRum MVP

## Status
- Postgres queue: working
- Worker: stable
- Bot: running
- Redis: active

## Architecture
- bot → Telegram entrypoint
- worker → PostgreSQL task consumer
- db → PostgreSQL queue storage
- redis → caching layer

## Queue table
tasks:
- id
- type
- payload
- status
- priority
- retries / max_retries

## Current state
Stable infrastructure ready for business logic (route search / flight API integration)
