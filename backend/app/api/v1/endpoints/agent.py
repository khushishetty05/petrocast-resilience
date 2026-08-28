from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.schemas.agent import AgentQueryRequest, AgentQueryResponse
from app.services.agent_service import run_agent_loop

router = APIRouter()

@router.post("/chat", response_model=AgentQueryResponse)
async def agent_chat_endpoint(
    req: AgentQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Executes an autonomous ReAct loop with Gemini, granting the AI access 
    to all backend Petrocast tools to answer complex procurement queries.
    """
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not set in the environment.")
        
    try:
        return await run_agent_loop(req, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

