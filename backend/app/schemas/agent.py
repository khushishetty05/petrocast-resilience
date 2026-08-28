from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AgentQueryRequest(BaseModel):
    message: str
    current_stock_barrels: Optional[float] = None
    daily_consumption_barrels: Optional[float] = None
    storage_capacity_barrels: Optional[float] = None

class AgentQueryResponse(BaseModel):
    response: str
    tool_calls_executed: List[str]
    execution_steps: List[Dict[str, Any]]
