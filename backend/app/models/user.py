from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # API usage tracking
    daily_requests_count = Column(Integer, default=0)
    last_request_date = Column(DateTime(timezone=True))
    
    # Relationships
    projects = relationship("Project", back_populates="owner")
    generations = relationship("ContentGeneration", back_populates="user")
    marketing_plans = relationship("MarketingPlan", back_populates="user")