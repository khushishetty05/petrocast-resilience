from typing import List, Dict, Any, Literal
from pydantic import BaseModel

class Chokepoint(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    baseline_risk_score: float # 0.0 to 10.0 scale
    primary_commodity_flow: str

class ChokepointRiskResponse(BaseModel):
    chokepoint_id: str
    name: str
    current_risk_score: float
    status: Literal["LOW", "ELEVATED", "SEVERE", "CRITICAL"]
    risk_factors: List[str]
    geojson_feature: Dict[str, Any]
    is_vix_stale: bool = False
