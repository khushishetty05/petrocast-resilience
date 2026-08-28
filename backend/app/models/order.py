from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volume_barrels = Column(Float, nullable=False)
    status = Column(String, nullable=False, index=True) # e.g. 'PENDING', 'EXECUTED'
    execution_price = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
