from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
from typing import List

from app.db.database import get_db
from app.models.market import MarketTicker
from app.schemas.market import MarketDataResponse
from app.core.config import settings

router = APIRouter()

@router.get("/live", response_model=List[MarketDataResponse])
async def get_live_market(db: AsyncSession = Depends(get_db)):
    """
    Get live market data. 
    Strict fail-closed logic: If data is older than STALE_DATA_THRESHOLD_MINUTES,
    returns HTTP 503 Service Unavailable instead of returning stale/fallback data.
    """
    
    # Get the latest entry for each symbol
    # Distinct on symbol requires an order by symbol
    stmt = (
        select(MarketTicker)
        .order_by(MarketTicker.symbol, MarketTicker.timestamp.desc())
        .distinct(MarketTicker.symbol)
    )
    result = await db.execute(stmt)
    tickers = result.scalars().all()
    
    if not tickers:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="DATA_UNAVAILABLE: No market data exists in the database."
        )

    responses = []
    now = datetime.now(timezone.utc)
    threshold = timedelta(minutes=settings.STALE_DATA_THRESHOLD_MINUTES)
    
    for t in tickers:
        # Check staleness
        # Ensure timestamp is aware
        ts = t.timestamp if t.timestamp.tzinfo else t.timestamp.replace(tzinfo=timezone.utc)
        
        is_stale = (now - ts) > threshold
        
        if is_stale:
            # Enforce fail-closed mechanism
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"DATA_UNAVAILABLE: Market data for {t.symbol} is stale. Last updated at {ts}."
            )
            
        responses.append(
            MarketDataResponse(
                symbol=t.symbol,
                price=t.price,
                timestamp=ts,
                is_stale=False
            )
        )
        
    return responses
