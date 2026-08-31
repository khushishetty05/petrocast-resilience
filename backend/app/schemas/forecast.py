from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ForecastPoint(BaseModel):
    horizon: str
    date: str
    p10: float
    p50: float
    p90: float
    range: List[float]

class PriceForecastResponse(BaseModel):
    id: int
    symbol: str
    timestamp: datetime
    base_price: float
    vix_value: float
    
    p10: Optional[float] = None
    p50: Optional[float] = None
    p90: Optional[float] = None

    pred_1d_10th: float
    pred_1d_50th: float
    pred_1d_90th: float
    
    pred_1m_10th: float
    pred_1m_50th: float
    pred_1m_90th: float
    
    pred_3m_10th: float
    pred_3m_50th: float
    pred_3m_90th: float
    
    forecast_points: List[ForecastPoint] = []

    class Config:
        from_attributes = True
