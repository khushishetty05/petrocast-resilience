from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import market, procurement, chokepoint, rag, agent, forecast
from app.services.market_data_client import init_scheduler
from app.initial_data import seed_initial_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Seed fallback data
    await seed_initial_data()
    # Start scheduler
    scheduler = init_scheduler()
    scheduler.start()
    yield
    # Shutdown scheduler
    scheduler.shutdown()

app = FastAPI(
    title="Petrocast Resilience V2",
    description="Energy Procurement Platform",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router, prefix="/api/v1/market", tags=["Market"])
app.include_router(procurement.router, prefix="/api/v1/procurement", tags=["Procurement"])
app.include_router(chokepoint.router, prefix="/api/v1/chokepoints", tags=["Chokepoints"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(agent.router, prefix="/api/v1/agent", tags=["Agent"])
app.include_router(forecast.router, prefix="/api/v1/forecast", tags=["Price Forecasting"])

from fastapi.routing import APIRoute

# Safely print all registered API routes
for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"Path: {route.path} | Methods: {route.methods}")