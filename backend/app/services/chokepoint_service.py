from typing import List, Dict, Any
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.market import MarketTicker
from app.schemas.chokepoint import Chokepoint, ChokepointRiskResponse
from app.core.config import settings

# Static Baseline Data
CHOKEPOINTS = [
    Chokepoint(id="HORMUZ", name="Strait of Hormuz", latitude=26.5667, longitude=56.2500, baseline_risk_score=7.5, primary_commodity_flow="Crude Oil & LNG"),
    Chokepoint(id="SUEZ", name="Suez Canal", latitude=30.5852, longitude=32.2654, baseline_risk_score=5.0, primary_commodity_flow="Crude Oil & Refined Products"),
    Chokepoint(id="BAB_EL_MANDEB", name="Bab-el-Mandeb Strait", latitude=12.5833, longitude=43.3333, baseline_risk_score=8.0, primary_commodity_flow="Crude Oil"),
    Chokepoint(id="MALACCA", name="Strait of Malacca", latitude=1.4300, longitude=103.0000, baseline_risk_score=3.0, primary_commodity_flow="Crude Oil & Products")
]

async def _get_vix_status(db: AsyncSession) -> tuple[float | None, bool]:
    """Returns (vix_level, is_stale). Doesn't raise 503 so we can fallback."""
    stmt = (
        select(MarketTicker)
        .where(MarketTicker.symbol == "VIX")
        .order_by(MarketTicker.timestamp.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    ticker = result.scalar_one_or_none()

    if not ticker:
        return None, True

    now = datetime.now(timezone.utc)
    ts = ticker.timestamp if ticker.timestamp.tzinfo else ticker.timestamp.replace(tzinfo=timezone.utc)
    is_stale = (now - ts) > timedelta(minutes=settings.STALE_DATA_THRESHOLD_MINUTES)
    
    return ticker.price, is_stale

def _score_to_status(score: float) -> str:
    if score < 4.0: return "LOW"
    if score < 7.0: return "ELEVATED"
    if score < 8.5: return "SEVERE"
    return "CRITICAL"

def _build_geojson_feature(cp: Chokepoint, score: float, status: str) -> Dict[str, Any]:
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [cp.longitude, cp.latitude] # GeoJSON uses Long, Lat
        },
        "properties": {
            "id": cp.id,
            "name": cp.name,
            "risk_score": score,
            "status": status,
            "flow": cp.primary_commodity_flow
        }
    }

async def get_chokepoint_risks(db: AsyncSession) -> List[ChokepointRiskResponse]:
    vix_level, is_vix_stale = await _get_vix_status(db)
    
    responses = []
    
    for cp in CHOKEPOINTS:
        current_score = cp.baseline_risk_score
        risk_factors = [f"Baseline structural risk: {cp.baseline_risk_score}"]
        
        if is_vix_stale or vix_level is None:
            risk_factors.append("WARNING: Live market volatility (VIX) unavailable or stale. Falling back to baseline score.")
        else:
            # Dynamic overlay
            if vix_level > 20:
                multiplier = 1.0 + ((vix_level - 20) / 100.0) # E.g., VIX 30 -> 1.1x multiplier
                current_score = min(10.0, current_score * multiplier)
                risk_factors.append(f"High market volatility (VIX: {vix_level:.2f}) inflating risk score.")
            else:
                risk_factors.append(f"Stable market volatility (VIX: {vix_level:.2f}). No inflation applied.")

        # Round score
        current_score = round(current_score, 2)
        status = _score_to_status(current_score)
        
        geojson = _build_geojson_feature(cp, current_score, status)
        
        responses.append(
            ChokepointRiskResponse(
                chokepoint_id=cp.id,
                name=cp.name,
                current_risk_score=current_score,
                status=status,
                risk_factors=risk_factors,
                geojson_feature=geojson,
                is_vix_stale=is_vix_stale
            )
        )
        
    return responses

async def get_chokepoints_geojson(db: AsyncSession) -> Dict[str, Any]:
    """Returns a full GeoJSON FeatureCollection."""
    risks = await get_chokepoint_risks(db)
    
    features = [r.geojson_feature for r in risks]
    
    return {
        "type": "FeatureCollection",
        "features": features
    }
