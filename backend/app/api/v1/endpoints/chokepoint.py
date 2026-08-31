from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.chokepoint import ChokepointRiskResponse
from app.services.chokepoint_service import get_chokepoint_risks, get_chokepoints_geojson

router = APIRouter()

@router.get("/live", response_model=List[ChokepointRiskResponse])
@router.get("/risks", response_model=List[ChokepointRiskResponse])
async def get_live_chokepoints(db: AsyncSession = Depends(get_db)):
    """
    Returns all maritime chokepoints with dynamic risk scores based on live market volatility.
    Falls back to static baselines if market data is stale.
    """
    return await get_chokepoint_risks(db)

@router.get("/geojson", response_model=Dict[str, Any])
async def get_chokepoints_geojson_endpoint(db: AsyncSession = Depends(get_db)):
    """
    Returns a GeoJSON FeatureCollection of all chokepoints with embedded risk properties,
    suitable for frontend map rendering.
    """
    return await get_chokepoints_geojson(db)
