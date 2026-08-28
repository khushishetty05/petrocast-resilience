from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    current_stock_barrels = Column(Float, nullable=False)
    daily_consumption_barrels = Column(Float, nullable=False)
    storage_capacity_barrels = Column(Float, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
