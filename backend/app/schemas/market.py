from datetime import datetime
from pydantic import BaseModel

class MarketDataResponse(BaseModel):
    symbol: str
    price: float
    timestamp: datetime
    is_stale: bool
