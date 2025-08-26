from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class ContentType(enum.Enum):
    TEXT_TO_IMAGE = "text_to_image"
    PRODUCT_3D_RENDER = "product_3d_render"
    PROFESSIONAL_PRODUCT = "professional_product"
    SEO_CAPTION = "seo_caption"
    CONTENT_PLAN = "content_plan"
    MARKETING_PLAN = "marketing_plan"

class GenerationStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ContentGeneration(Base):
    __tablename__ = "content_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    source_image_id = Column(Integer, ForeignKey("product_images.id"), nullable=True)
    
    # Generation details
    content_type = Column(Enum(ContentType), nullable=False)
    status = Column(Enum(GenerationStatus), default=GenerationStatus.PENDING)
    prompt = Column(Text)
    parameters = Column(JSON)  # Store generation parameters (style, aspect ratio, etc.)
    
    # Results
    generated_content = Column(Text)  # For text content
    generated_image_path = Column(String)  # For image content
    generation_metadata = Column(JSON)  # Store additional metadata
    
    # AI Model info
    model_used = Column(String)
    api_key_used = Column(String)  # Track which API key was used
    processing_time = Column(Integer)  # Processing time in seconds
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="generations")
    project = relationship("Project", back_populates="generations")
    source_image = relationship("ProductImage", back_populates="generations")

class MarketingGoal(enum.Enum):
    OUTREACH = "outreach"
    SALES = "sales"
    BRANDING = "branding"

class MarketingPlan(Base):
    __tablename__ = "marketing_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    # Plan details
    goal = Column(Enum(MarketingGoal), nullable=False)
    target_audience = Column(Text)
    budget_range = Column(String)
    timeline = Column(String)
    
    # Generated content
    strategy = Column(Text)
    tactics = Column(JSON)  # List of marketing tactics
    content_calendar = Column(JSON)  # Monthly/weekly content plan
    seo_keywords = Column(JSON)  # Recommended keywords
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="marketing_plans")
    project = relationship("Project", back_populates="marketing_plans")

class SEOAnalysis(Base):
    __tablename__ = "seo_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    
    # SEO data
    keywords = Column(JSON)  # Primary and secondary keywords
    competitor_analysis = Column(JSON)
    content_suggestions = Column(JSON)
    meta_descriptions = Column(JSON)
    hashtag_recommendations = Column(JSON)
    
    # Performance metrics
    search_volume = Column(JSON)
    competition_level = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())