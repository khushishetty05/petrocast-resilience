import uuid
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False, unique=True)
    country = Column(String, nullable=False)
    reliability_score = Column(Float, nullable=False)
    freight_cost = Column(Float, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
