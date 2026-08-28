from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.schemas.rag import NewsIngestRequest, RAGQueryRequest, RAGQueryResponse
from app.services.rag_service import ingest_article, query_news

router = APIRouter()

@router.post("/ingest")
def ingest_news_endpoint(req: NewsIngestRequest) -> Dict[str, str]:
    """Ingests a single maritime news article into the ChromaDB vector store."""
    try:
        article_id = ingest_article(req)
        return {"status": "success", "article_id": article_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=RAGQueryResponse)
def query_news_endpoint(req: RAGQueryRequest):
    """
    Retrieves grounded context for the provided question.
    Enforces a strict similarity threshold to prevent hallucinations.
    """
    try:
        return query_news(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seed")
def seed_news_endpoint() -> Dict[str, Any]:
    """Seeds the ChromaDB vector store with 5 sample geopolitical maritime news articles."""
    try:
        samples = [
            NewsIngestRequest(
                title="Houthi Rebels Target Tanker in Red Sea",
                content="A crude oil tanker was struck by a drone near the Bab-el-Mandeb strait today. The vessel sustained minor damage but no casualties were reported. Analysts warn of increasing freight costs for the region.",
                source="Maritime Executive",
                publish_date="2026-08-01",
                chokepoint_tag="BAB_EL_MANDEB"
            ),
            NewsIngestRequest(
                title="Suez Canal Authorities Announce Toll Hike",
                content="The Suez Canal Authority has announced a 15% increase in transit tolls for crude oil tankers effective next month. This is expected to slightly increase the landed cost of Middle Eastern crude in Europe.",
                source="Reuters",
                publish_date="2026-08-03",
                chokepoint_tag="SUEZ"
            ),
            NewsIngestRequest(
                title="Naval Drills in Strait of Hormuz Escalate Tensions",
                content="Unscheduled naval drills by Iranian forces in the Strait of Hormuz have temporarily slowed vessel traffic. While no blockade is in place, insurance premiums for the corridor have spiked.",
                source="Bloomberg",
                publish_date="2026-08-05",
                chokepoint_tag="HORMUZ"
            ),
            NewsIngestRequest(
                title="Piracy Incident Thwarted near Strait of Malacca",
                content="Regional coast guards successfully thwarted a boarding attempt on an LNG carrier transiting the Strait of Malacca. Patrols have been increased to ensure safe passage.",
                source="Lloyds List",
                publish_date="2026-07-28",
                chokepoint_tag="MALACCA"
            ),
            NewsIngestRequest(
                title="OPEC+ Agrees to Maintain Production Cuts",
                content="OPEC+ delegates reached an agreement in Vienna today to roll over existing production cuts into the next quarter, aiming to stabilize global crude prices amidst macroeconomic uncertainty.",
                source="Financial Times",
                publish_date="2026-08-04",
                chokepoint_tag="GENERAL"
            )
        ]
        
        for sample in samples:
            ingest_article(sample)
            
        return {"status": "success", "articles_seeded": len(samples)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to seed RAG database: {str(e)}")
