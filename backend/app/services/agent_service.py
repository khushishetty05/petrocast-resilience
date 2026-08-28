import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from google import genai
from google.genai import types

from app.models.market import MarketTicker
from app.schemas.procurement import ProcurementRequest
from app.schemas.rag import RAGQueryRequest
from app.services.procurement_engine import calculate_procurement_recommendation
from app.services.chokepoint_service import get_chokepoint_risks
from app.services.rag_service import query_news

from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.core.config import settings
from app.services.agent_tools import (
    get_live_market_data_tool,
    run_procurement_math_tool,
    get_chokepoint_risks_tool,
    query_maritime_news_tool,
    get_price_forecast_tool
)

logger = logging.getLogger(__name__)

async def run_agent_loop(req: AgentQueryRequest, db: AsyncSession) -> AgentQueryResponse:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    available_tools = [
        get_live_market_data_tool,
        run_procurement_math_tool,
        get_chokepoint_risks_tool,
        query_maritime_news_tool,
        get_price_forecast_tool
    ]
    
    system_instruction = (
        "You are an autonomous supply chain intelligence agent for Petrocast. "
        "You MUST invoke available tools (get_live_market_data_tool, run_procurement_math_tool, "
        "get_chokepoint_risks_tool, query_maritime_news_tool, get_price_forecast_tool) to gather live facts before answering. "
        "Never state data is unavailable without calling the corresponding tool first.\n\n"
        "FORMATTING RULES:\n"
        "1. Do NOT use markdown asterisks (**) anywhere in your response.\n"
        "2. Structure every response into 3 clean plain-text sections with uppercase headers:\n"
        "   OPERATIONAL STATUS:\n"
        "   - Current stock and days of cover remaining.\n\n"
        "   MARKET & RISK METRICS:\n"
        "   - Key prices, p90 risk, and shipping delays.\n\n"
        "   ACTION PLAN:\n"
        "   - 1-2 direct procurement steps.\n"
        "3. Keep total output under 100 words."
    )
    
    config = types.GenerateContentConfig(
        tools=available_tools,
        system_instruction=system_instruction,
        temperature=0.1,
    )
    
    prompt = f"User Request: {req.message}\n"
    if req.current_stock_barrels is not None:
        prompt += (
            f"Context - Current Stock: {req.current_stock_barrels} bbls, "
            f"Daily Consumption: {req.daily_consumption_barrels} bbls, "
            f"Storage Capacity: {req.storage_capacity_barrels} bbls.\n"
        )
        
    execution_steps = []
    tool_calls_executed = []
    
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]
    
    max_iterations = 4
    iteration = 0
    final_text = "Agent finished execution."
    
    while iteration < max_iterations:
        iteration += 1
        
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=contents,
            config=config
        )
        
        if response.candidates and response.candidates[0].content:
            contents.append(response.candidates[0].content)
        
        if response.function_calls:
            function_responses_parts = []
            
            for fc in response.function_calls:
                tool_name = fc.name
                args = dict(fc.args) if fc.args else {}
                
                tool_calls_executed.append(tool_name)
                
                step = {
                    "thought": f"Calling tool {tool_name}",
                    "action": tool_name,
                    "args": args
                }
                
                try:
                    if tool_name == "get_live_market_data_tool":
                        stmt = select(MarketTicker).order_by(MarketTicker.symbol, MarketTicker.timestamp.desc()).distinct(MarketTicker.symbol)
                        res = await db.execute(stmt)
                        tickers = res.scalars().all()
                        if not tickers:
                            result = "No market data available."
                        else:
                            data = []
                            now = datetime.now(timezone.utc)
                            for t in tickers:
                                ts = t.timestamp if t.timestamp.tzinfo else t.timestamp.replace(tzinfo=timezone.utc)
                                is_stale = (now - ts).total_seconds() > (15 * 60)
                                data.append(f"{t.symbol}: {t.price} {'(STALE)' if is_stale else '(LIVE)'}")
                            result = "\n".join(data)

                    elif tool_name == "run_procurement_math_tool":
                        proc_req = ProcurementRequest(
                            current_stock_barrels=args.get("current_stock"),
                            daily_consumption_barrels=args.get("daily_consumption"),
                            storage_capacity_barrels=args.get("storage_capacity"),
                            target_buffer_days=args.get("target_buffer_days", 15),
                            risk_tolerance=args.get("risk_tolerance", "BALANCED")
                        )
                        resp = await calculate_procurement_recommendation(proc_req, db)
                        result = (
                            f"Recommendation: {resp.recommendation}\n"
                            f"Urgency: {resp.urgency_level}\n"
                            f"Actionable Volume: {resp.recommended_buy_volume_barrels} bbls\n"
                            f"Estimated Cost: ${resp.estimated_cost_usd}\n"
                            f"Reasoning: {' '.join(resp.reasoning)}"
                        )

                    elif tool_name == "get_chokepoint_risks_tool":
                        risks = await get_chokepoint_risks(db)
                        out = []
                        for r in risks:
                            out.append(f"{r.name}: Score {r.current_risk_score}/10 ({r.status}) - {', '.join(r.risk_factors)}")
                        result = "\n".join(out)

                    elif tool_name == "query_maritime_news_tool":
                        rag_req = RAGQueryRequest(question=args.get("query_text"), top_k=2)
                        resp = query_news(rag_req)
                        if not resp.is_relevant:
                            result = "No relevant maritime news found in database."
                        else:
                            result = f"Context: {' '.join(resp.answer_context)}\nSources: {', '.join(resp.sources)}"

                    elif tool_name == "get_price_forecast_tool":
                        from app.services.forecast_service import generate_quantile_forecast
                        resp = await generate_quantile_forecast(args.get("symbol", "BZ=F"), db)
                        result = (
                            f"Forecast for {resp.symbol} (Base Price: ${resp.base_price:.2f}, VIX: {resp.vix_value:.2f}):\n"
                            f"1-Day: p10=${resp.pred_1d_10th:.2f}, p50=${resp.pred_1d_50th:.2f}, p90=${resp.pred_1d_90th:.2f}\n"
                            f"1-Month: p10=${resp.pred_1m_10th:.2f}, p50=${resp.pred_1m_50th:.2f}, p90=${resp.pred_1m_90th:.2f}\n"
                            f"3-Month: p10=${resp.pred_3m_10th:.2f}, p50=${resp.pred_3m_50th:.2f}, p90=${resp.pred_3m_90th:.2f}"
                        )

                    else:
                        result = f"Error: Tool {tool_name} not found."
                except Exception as e:
                    logger.error(f"Error executing {tool_name}: {e}")
                    result = f"Error executing {tool_name}: {str(e)}"
                    
                step["observation"] = str(result)
                execution_steps.append(step)
                
                function_responses_parts.append(
                    types.Part.from_function_response(
                        name=tool_name, 
                        response={"result": result}
                    )
                )
            
            contents.append(
                types.Content(
                    role="user",
                    parts=function_responses_parts
                )
            )
        else:
            final_text = response.text if response.text else "Agent finished execution."
            break

    return AgentQueryResponse(
        response=final_text,
        tool_calls_executed=tool_calls_executed,
        execution_steps=execution_steps
    )
