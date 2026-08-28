from pydantic import BaseModel
from datetime import datetime

class PriceForecastResponse(BaseModel):
    id: int
    symbol: str
    timestamp: datetime
    base_price: float
    vix_value: float
    
    pred_1d_10th: float
    pred_1d_50th: float
    pred_1d_90th: float
    
    pred_1m_10th: float
    pred_1m_50th: float
    pred_1m_90th: float
    
    pred_3m_10th: float
    pred_3m_50th: float
    pred_3m_90th: float

    class Config:
        from_attributes = True
