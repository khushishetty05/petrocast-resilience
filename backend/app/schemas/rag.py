from typing import List
from pydantic import BaseModel

class NewsIngestRequest(BaseModel):
    title: str
    content: str
    source: str
    publish_date: str
    chokepoint_tag: str  # e.g., "HORMUZ", "SUEZ", "BAB_EL_MANDEB", "MALACCA", "GENERAL"

class RAGQueryRequest(BaseModel):
    question: str
    top_k: int = 3

class RAGQueryResponse(BaseModel):
    query: str
    answer_context: List[str]
    sources: List[str]
    is_relevant: bool
