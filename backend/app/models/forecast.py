from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.models.base import Base

class PriceForecast(Base):
    __tablename__ = "price_forecasts"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    base_price = Column(Float, nullable=False)
    vix_value = Column(Float, nullable=False)
    
    # 1-Day Horizon
    pred_1d_10th = Column(Float, nullable=False)
    pred_1d_50th = Column(Float, nullable=False)
    pred_1d_90th = Column(Float, nullable=False)
    
    # 1-Month Horizon (21 trading days)
    pred_1m_10th = Column(Float, nullable=False)
    pred_1m_50th = Column(Float, nullable=False)
    pred_1m_90th = Column(Float, nullable=False)
    
    # 3-Month Horizon (63 trading days)
    pred_3m_10th = Column(Float, nullable=False)
    pred_3m_50th = Column(Float, nullable=False)
    pred_3m_90th = Column(Float, nullable=False)
