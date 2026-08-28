import logging
import asyncio
from datetime import datetime, timezone
import yfinance as yf
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.db.database import async_session_maker
from app.models.market import MarketTicker

logger = logging.getLogger(__name__)

SYMBOLS = {
    "BZ=F": "Brent",
    "CL=F": "WTI",
    "^VIX": "VIX",
    "GC=F": "Gold",
    "INR=X": "USD/INR"
}

async def fetch_and_save_tickers():
    logger.info("Fetching market tickers...")
    try:
        data = yf.download(list(SYMBOLS.keys()), period="1d", group_by="ticker")
        
        async with async_session_maker() as session:
            for yf_symbol, internal_name in SYMBOLS.items():
                try:
                    # Depending on yfinance version, the structure of 'data' might vary when fetching multiple symbols.
                    # Standard yf.download with multiple tickers and group_by='ticker' returns a MultiIndex column DataFrame.
                    ticker_data = data[yf_symbol] if len(SYMBOLS) > 1 else data
                    if ticker_data.empty:
                        logger.warning(f"No data returned for {internal_name} ({yf_symbol})")
                        continue
                        
                    last_price = float(ticker_data['Close'].iloc[-1])
                    
                    ticker_record = MarketTicker(
                        symbol=internal_name,
                        price=last_price,
                        provider="yfinance"
                    )
                    session.add(ticker_record)
                except Exception as e:
                    logger.error(f"Error processing {yf_symbol}: {e}")
                    
            await session.commit()
            logger.info("Successfully saved market tickers.")
    except Exception as e:
        logger.error(f"Failed to fetch market data: {e}")

def init_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    # Run immediately, then every X minutes
    scheduler.add_job(
        fetch_and_save_tickers, 
        'interval', 
        minutes=settings.MARKET_POLL_INTERVAL_MINUTES,
        next_run_time=datetime.now(timezone.utc)
    )
    return scheduler
