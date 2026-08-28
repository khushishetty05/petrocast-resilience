import logging
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.market import MarketTicker
from app.schemas.procurement import ProcurementRequest, ProcurementResponse
from app.core.config import settings

logger = logging.getLogger(__name__)

async def _get_latest_ticker(db: AsyncSession, symbol: str) -> float:
    """Fetch the latest ticker price with fail-closed protection."""
    stmt = (
        select(MarketTicker)
        .where(MarketTicker.symbol == symbol)
        .order_by(MarketTicker.timestamp.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    ticker = result.scalar_one_or_none()

    if not ticker:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"DATA_UNAVAILABLE: No market data found for {symbol}"
        )

    now = datetime.now(timezone.utc)
    # Ensure timestamp is tz-aware
    ts = ticker.timestamp if ticker.timestamp.tzinfo else ticker.timestamp.replace(tzinfo=timezone.utc)
    
    if (now - ts) > timedelta(minutes=settings.STALE_DATA_THRESHOLD_MINUTES):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"DATA_UNAVAILABLE: {symbol} data is stale (older than {settings.STALE_DATA_THRESHOLD_MINUTES} min)."
        )
        
    return ticker.price

async def calculate_procurement_recommendation(
    req: ProcurementRequest, 
    db: AsyncSession
) -> ProcurementResponse:
    
    # 1. Fetch live market signals
    brent_price = await _get_latest_ticker(db, "Brent")
    vix_level = await _get_latest_ticker(db, "VIX")
    
    # 2. Base Math
    days_remaining = req.current_stock_barrels / req.daily_consumption_barrels
    fill_capacity = req.storage_capacity_barrels - req.current_stock_barrels
    
    recommendation = "HOLD"
    urgency_level = "LOW"
    recommended_buy_volume = 0.0
    reasoning = []
    
    reasoning.append(f"Current inventory cover: {days_remaining:.1f} days.")
    reasoning.append(f"Live Brent Price: ${brent_price:.2f}/bbl. Live VIX: {vix_level:.2f}.")

    # 3. Deterministic Decision Tree
    if days_remaining < 5:
        recommendation = "CRITICAL_REFILL"
        urgency_level = "CRITICAL"
        # Buy enough to reach target buffer
        target_volume = (req.target_buffer_days * req.daily_consumption_barrels) - req.current_stock_barrels
        recommended_buy_volume = min(target_volume, fill_capacity)
        reasoning.append("Inventory is critically low (under 5 days). Triggering immediate refill regardless of market conditions.")
    else:
        if vix_level < 20:
            # Low volatility
            recommendation = "BUY_NOW"
            urgency_level = "MEDIUM"
            # Top up storage or target buffer
            target_volume = (req.target_buffer_days * req.daily_consumption_barrels) - req.current_stock_barrels
            recommended_buy_volume = min(target_volume, fill_capacity) if target_volume > 0 else 0
            reasoning.append("Market volatility is low (VIX < 20). Recommended to lock in prices and build inventory.")
        else:
            # High volatility
            reasoning.append("High market volatility detected (VIX >= 20). Spike risk is elevated.")
            if req.risk_tolerance == "CONSERVATIVE":
                recommendation = "HEDGE"
                urgency_level = "HIGH"
                # Split the difference, buy 50% of target
                target_volume = (req.target_buffer_days * req.daily_consumption_barrels) - req.current_stock_barrels
                recommended_buy_volume = min(target_volume * 0.5, fill_capacity) if target_volume > 0 else 0
                reasoning.append("Conservative risk tolerance: Hedging exposure by purchasing 50% of the target buffer.")
            elif req.risk_tolerance == "AGGRESSIVE":
                recommendation = "HOLD"
                urgency_level = "LOW"
                recommended_buy_volume = 0
                reasoning.append("Aggressive risk tolerance: Holding off purchases to draw down existing stock and wait for price crash.")
            else:
                # BALANCED
                recommendation = "HOLD"
                urgency_level = "MEDIUM"
                recommended_buy_volume = 0
                reasoning.append("Balanced risk tolerance: Holding off major purchases to avoid volatility spikes.")

    # 4. Financial impact calculation
    estimated_cost_usd = recommended_buy_volume * brent_price

    return ProcurementResponse(
        recommendation=recommendation,
        urgency_level=urgency_level,
        days_remaining=days_remaining,
        recommended_buy_volume_barrels=recommended_buy_volume,
        estimated_cost_usd=estimated_cost_usd,
        reasoning=reasoning
    )
