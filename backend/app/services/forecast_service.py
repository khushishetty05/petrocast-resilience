import math
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone
from app.models.market import MarketTicker
from app.models.forecast import PriceForecast
from app.schemas.forecast import PriceForecastResponse

logger = logging.getLogger(__name__)

def normalize_symbol(sym: str) -> str:
    s = sym.upper()
    if s in ["BZ=F", "BRENT"]:
        return "Brent"
    if s in ["CL=F", "WTI"]:
        return "WTI"
    if s in ["^VIX", "VIX"]:
        return "VIX"
    return sym

async def generate_quantile_forecast(symbol: str, db: AsyncSession) -> PriceForecastResponse:
    norm_symbol = normalize_symbol(symbol)
    
    # Fetch latest base price using case-insensitive match
    stmt = select(MarketTicker).where(func.lower(MarketTicker.symbol) == norm_symbol.lower()).order_by(MarketTicker.timestamp.desc()).limit(1)
    res = await db.execute(stmt)
    base_ticker = res.scalar_one_or_none()
    
    # Fetch latest VIX using case-insensitive match
    stmt_vix = select(MarketTicker).where(func.lower(MarketTicker.symbol) == "vix").order_by(MarketTicker.timestamp.desc()).limit(1)
    res_vix = await db.execute(stmt_vix)
    vix_ticker = res_vix.scalar_one_or_none()
    
    if not base_ticker:
        logger.error(f"Missing market data for base asset: {norm_symbol}")
    if not vix_ticker:
        logger.error("Missing market data for volatility benchmark: VIX")
        
    if not base_ticker or not vix_ticker:
        raise ValueError(f"Missing market data for forecasting. Base: {norm_symbol}={'Found' if base_ticker else 'Missing'}, VIX={'Found' if vix_ticker else 'Missing'}")
        
    base_price = base_ticker.price
    vix = vix_ticker.price
    
    # Daily volatility from VIX
    daily_vol = (vix / 100.0) / math.sqrt(252)
    
    def calculate_bounds(days: int):
        # 1.28 is the 10th/90th percentile of a standard normal distribution
        drift = 1.28 * daily_vol * math.sqrt(days)
        p10 = base_price * math.exp(-drift)
        p50 = base_price
        p90 = base_price * math.exp(drift)
        return p10, p50, p90
        
    p1d_10, p1d_50, p1d_90 = calculate_bounds(1)
    p1m_10, p1m_50, p1m_90 = calculate_bounds(21)
    p3m_10, p3m_50, p3m_90 = calculate_bounds(63)
    
    forecast = PriceForecast(
        symbol=symbol,
        base_price=base_price,
        vix_value=vix,
        pred_1d_10th=p1d_10,
        pred_1d_50th=p1d_50,
        pred_1d_90th=p1d_90,
        pred_1m_10th=p1m_10,
        pred_1m_50th=p1m_50,
        pred_1m_90th=p1m_90,
        pred_3m_10th=p3m_10,
        pred_3m_50th=p3m_50,
        pred_3m_90th=p3m_90
    )
    
    db.add(forecast)
    await db.commit()
    await db.refresh(forecast)
    
    return PriceForecastResponse.model_validate(forecast)
