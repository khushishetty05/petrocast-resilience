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
        raise ValueError(f"Missing market data for forecasting. Base: {norm_symbol}=Missing")
        
    raw_base = base_ticker.price if base_ticker else None
    if raw_base is None or math.isnan(float(raw_base)) or float(raw_base) <= 0:
        base_price = 82.50 if norm_symbol == "Brent" else (78.20 if norm_symbol == "WTI" else 80.0)
        logger.warning(f"Invalid base price {raw_base} for {norm_symbol}. Falling back to ${base_price}")
    else:
        base_price = float(raw_base)

    raw_vix = vix_ticker.price if vix_ticker else None
    if raw_vix is None or math.isnan(float(raw_vix)) or float(raw_vix) <= 0:
        vix = 15.5
        logger.warning(f"Invalid VIX {raw_vix}. Falling back to default_vix = 15.5")
    else:
        vix = float(raw_vix)
    
    # Daily volatility from VIX
    daily_vol = (vix / 100.0) / math.sqrt(252)
    
    def calculate_bounds(days: int):
        # 1.28 is the 10th/90th percentile of a standard normal distribution
        drift = 1.28 * daily_vol * math.sqrt(days)
        p10 = base_price * math.exp(-drift)
        p50 = base_price
        p90 = base_price * math.exp(drift)
        return float(p10), float(p50), float(p90)
        
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
    
    # Construct the frontend-aligned payload
    forecast_points = [
        {"horizon": "Current", "date": "Current", "p10": base_price, "p50": base_price, "p90": base_price, "range": [base_price, base_price]},
        {"horizon": "1 Day", "date": "1 Day", "p10": p1d_10, "p50": p1d_50, "p90": p1d_90, "range": [p1d_10, p1d_90]},
        {"horizon": "1 Month", "date": "1 Month", "p10": p1m_10, "p50": p1m_50, "p90": p1m_90, "range": [p1m_10, p1m_90]},
        {"horizon": "3 Months", "date": "3 Months", "p10": p3m_10, "p50": p3m_50, "p90": p3m_90, "range": [p3m_10, p3m_90]}
    ]
    
    response = PriceForecastResponse.model_validate(forecast)
    response.p10 = p1m_10
    response.p50 = p1m_50
    response.p90 = p1m_90
    response.forecast_points = forecast_points
    
    return response
