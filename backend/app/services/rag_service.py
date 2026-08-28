import os
import hashlib
import logging
from typing import List

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from app.schemas.rag import NewsIngestRequest, RAGQueryRequest, RAGQueryResponse

logger = logging.getLogger(__name__)

# Initialize ChromaDB Persistent Client
CHROMA_DIR = os.path.join(os.getcwd(), "chroma_db")
os.makedirs(CHROMA_DIR, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=CHROMA_DIR, settings=Settings(anonymized_telemetry=False))

# Use Sentence Transformers for local embeddings
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name="maritime_news",
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"} # Use cosine similarity
)

# Fail-Closed Threshold (Cosine distance: 0.0 is exact match, > 0.5 is getting irrelevant)
RELEVANCE_THRESHOLD = 0.6

def _generate_hash(title: str, content: str) -> str:
    """Generate a unique deterministic hash for the article to prevent duplicates."""
    return hashlib.sha256(f"{title}:{content}".encode('utf-8')).hexdigest()

def ingest_article(req: NewsIngestRequest) -> str:
    """Embeds and stores the article in ChromaDB."""
    article_id = _generate_hash(req.title, req.content)
    
    # Check if exists
    existing = collection.get(ids=[article_id])
    if existing and existing["ids"]:
        logger.info(f"Article '{req.title}' already exists. Skipping ingestion.")
        return article_id
        
    full_text = f"Title: {req.title}\nSource: {req.source}\nDate: {req.publish_date}\n\n{req.content}"
    
    collection.add(
        documents=[full_text],
        metadatas=[{
            "title": req.title,
            "source": req.source,
            "publish_date": req.publish_date,
            "chokepoint_tag": req.chokepoint_tag
        }],
        ids=[article_id]
    )
    
    logger.info(f"Ingested article: {req.title}")
    return article_id

def query_news(req: RAGQueryRequest) -> RAGQueryResponse:
    """Searches for relevant context and enforces Fail-Closed bounds."""
    results = collection.query(
        query_texts=[req.question],
        n_results=req.top_k
    )
    
    if not results or not results['distances'] or not results['distances'][0]:
        return RAGQueryResponse(
            query=req.question,
            answer_context=["No relevant maritime news found."],
            sources=[],
            is_relevant=False
        )
        
    # Check the top result's distance against the threshold
    top_distance = results['distances'][0][0]
    
    if top_distance > RELEVANCE_THRESHOLD:
        logger.warning(f"Fail-Closed: Top result distance {top_distance} exceeds threshold {RELEVANCE_THRESHOLD}")
        return RAGQueryResponse(
            query=req.question,
            answer_context=["No relevant maritime news found."],
            sources=[],
            is_relevant=False
        )
        
    # Compile context
    contexts = results['documents'][0]
    sources_raw = results['metadatas'][0]
    
    formatted_sources = []
    for meta in sources_raw:
        formatted_sources.append(f"{meta.get('source', 'Unknown')} ({meta.get('publish_date', 'N/A')}) - {meta.get('title', 'Unknown')}")
        
    return RAGQueryResponse(
        query=req.question,
        answer_context=contexts,
        sources=formatted_sources,
        is_relevant=True
    )
