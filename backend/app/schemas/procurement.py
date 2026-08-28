from typing import List, Literal
from pydantic import BaseModel, Field

class ProcurementRequest(BaseModel):
    current_stock_barrels: float = Field(..., ge=0)
    daily_consumption_barrels: float = Field(..., gt=0)
    storage_capacity_barrels: float = Field(..., gt=0)
    target_buffer_days: int = 15
    risk_tolerance: Literal["CONSERVATIVE", "BALANCED", "AGGRESSIVE"] = "BALANCED"

class ProcurementResponse(BaseModel):
    recommendation: Literal["BUY_NOW", "HOLD", "HEDGE", "CRITICAL_REFILL"]
    urgency_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    days_remaining: float
    recommended_buy_volume_barrels: float
    estimated_cost_usd: float
    reasoning: List[str]
