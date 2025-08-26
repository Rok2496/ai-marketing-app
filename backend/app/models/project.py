from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Project metadata
    product_category = Column(String)
    target_audience = Column(Text)
    brand_guidelines = Column(JSON)  # Store brand colors, fonts, style preferences
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    product_images = relationship("ProductImage", back_populates="project")
    generations = relationship("ContentGeneration", back_populates="project")
    marketing_plans = relationship("MarketingPlan", back_populates="project")

class ProductImage(Base):
    __tablename__ = "product_images"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Image metadata
    width = Column(Integer)
    height = Column(Integer)
    is_primary = Column(Boolean, default=False)  # Main product image
    
    # Relationships
    project = relationship("Project", back_populates="product_images")
    generations = relationship("ContentGeneration", back_populates="source_image")