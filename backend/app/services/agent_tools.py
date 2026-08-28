"""
These functions serve strictly as schema definitions for the Google Gemini SDK.
By keeping them as pure signatures with detailed docstrings and NO complex dependencies 
(like AsyncSession), we guarantee the google-genai schema parser will never crash.
The actual execution logic for these tools is handled inside agent_service.py's ReAct loop.
"""

async def get_live_market_data_tool() -> str:
    """Returns live market data for Brent Crude, WTI Crude, VIX, Gold, and USD/INR."""
    pass

async def run_procurement_math_tool(
    current_stock: float, 
    daily_consumption: float, 
    storage_capacity: float, 
    target_buffer_days: int = 15, 
    risk_tolerance: str = "BALANCED"
) -> str:
    """Calculates procurement requirements, stock cover days, urgency level, and order volume."""
    pass

async def get_chokepoint_risks_tool() -> str:
    """Returns dynamic risk scores and status for maritime chokepoints like Hormuz, Suez, and Bab-el-Mandeb."""
    pass

async def query_maritime_news_tool(query_text: str) -> str:
    """Queries ChromaDB vector store for relevant news regarding a specific maritime question or chokepoint."""
    pass

async def get_price_forecast_tool(symbol: str = "BZ=F") -> str:
    """Returns deterministic price forecasts (p10, p50, p90 quantiles) for 1-day, 1-month, and 3-month horizons based on current market volatility. Use for any future price prediction queries."""
    pass
