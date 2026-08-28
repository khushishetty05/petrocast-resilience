from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.procurement import ProcurementRequest, ProcurementResponse
from app.services.procurement_engine import calculate_procurement_recommendation

router = APIRouter()

@router.post("/calculate", response_model=ProcurementResponse)
async def calculate_procurement(
    request: ProcurementRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Calculate procurement recommendations based on user inventory and live market data.
    Enforces fail-closed logic if market tickers are stale or unavailable.
    """
    return await calculate_procurement_recommendation(request, db)
