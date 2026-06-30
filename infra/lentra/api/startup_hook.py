import asyncio
from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine
from lentra.core.market_intelligence.stream_processor.stream_processor import StreamProcessor


engine = MarketIntelligenceEngine()
processor = StreamProcessor(engine.event_bus, engine.state_store, engine)


async def start_background_stream():
    asyncio.create_task(processor.start())
