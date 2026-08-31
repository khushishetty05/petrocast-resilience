import asyncio
import logging
from datetime import datetime, timezone
from sqlalchemy import select
from app.db.database import async_session_maker
from app.models.market import MarketTicker
from app.models.forecast import PriceForecast

logger = logging.getLogger(__name__)

async def seed_initial_data():
    """Seeds the database with fallback data so the frontend doesn't crash if yfinance fails."""
    async with async_session_maker() as session:
        # Check if market tickers exist
        stmt = select(MarketTicker).limit(1)
        res = await session.execute(stmt)
        if not res.scalar_one_or_none():
            logger.info("Database is empty. Seeding initial baseline market data...")
            
            now = datetime.now(timezone.utc)
            
            # Default fallback prices
            defaults = [
                MarketTicker(symbol="Brent", price=82.50, provider="seed", timestamp=now),
                MarketTicker(symbol="WTI", price=78.20, provider="seed", timestamp=now),
                MarketTicker(symbol="VIX", price=15.40, provider="seed", timestamp=now),
                MarketTicker(symbol="Gold", price=2340.10, provider="seed", timestamp=now),
                MarketTicker(symbol="USD/INR", price=83.15, provider="seed", timestamp=now)
            ]
            session.add_all(defaults)
            
            # Default Forecasts
            brent_forecast = PriceForecast(
                symbol="Brent",
                base_price=82.50,
                vix_value=15.40,
                pred_1d_10th=81.10, pred_1d_50th=82.50, pred_1d_90th=83.90,
                pred_1m_10th=78.40, pred_1m_50th=82.50, pred_1m_90th=86.60,
                pred_3m_10th=72.10, pred_3m_50th=82.50, pred_3m_90th=92.90,
                timestamp=now
            )
            wti_forecast = PriceForecast(
                symbol="WTI",
                base_price=78.20,
                vix_value=15.40,
                pred_1d_10th=76.80, pred_1d_50th=78.20, pred_1d_90th=79.60,
                pred_1m_10th=74.30, pred_1m_50th=78.20, pred_1m_90th=82.10,
                pred_3m_10th=68.50, pred_3m_50th=78.20, pred_3m_90th=87.90,
                timestamp=now
            )
            session.add_all([brent_forecast, wti_forecast])
            
            await session.commit()
            logger.info("Successfully seeded database.")
        else:
            logger.info("Database already seeded.")
