from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.forecast import PriceForecastResponse
from app.services.forecast_service import generate_quantile_forecast

router = APIRouter()

@router.get("/latest/{symbol}", response_model=PriceForecastResponse)
async def get_latest_forecast(symbol: str, db: AsyncSession = Depends(get_db)):
    try:
        return await generate_quantile_forecast(symbol, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
