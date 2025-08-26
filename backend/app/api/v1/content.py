from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json
from datetime import datetime

from ...core.database import get_db
from ...models.user import User
from ...models.content import ContentGeneration, ContentType, GenerationStatus
from ...services.ai_service import ai_service
from .auth import get_current_active_user

router = APIRouter()

# Pydantic models
class TextToImageRequest(BaseModel):
    prompt: str
    style: str = "Realistic"
    aspect_ratio: str = "Square (1:1)"
    project_id: Optional[int] = None

class ProductRenderRequest(BaseModel):
    render_type: str = "3d_render"  # or "professional_product"
    instructions: str = ""
    project_id: Optional[int] = None

class SEOContentRequest(BaseModel):
    product_description: str
    target_keywords: List[str] = []
    platform: str = "general"
    project_id: Optional[int] = None

class ContentPlanRequest(BaseModel):
    product_info: str
    target_audience: str
    goals: List[str]
    timeframe: str = "monthly"
    project_id: Optional[int] = None

class MarketingPlanRequest(BaseModel):
    product_info: str
    target_audience: str
    goal: str  # outreach, sales, branding
    budget_range: str
    timeline: str
    project_id: Optional[int] = None

class ContentGenerationResponse(BaseModel):
    id: int
    content_type: str
    status: str
    generated_content: Optional[str]
    generated_image_path: Optional[str]
    generation_metadata: Optional[dict] = None  # FIXED: Added this field
    model_used: Optional[str]
    processing_time: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/text-to-image", response_model=ContentGenerationResponse)
async def generate_text_to_image(
    request: TextToImageRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Generate image from text prompt"""
    
    # Create generation record
    generation = ContentGeneration(
        user_id=current_user.id,
        project_id=request.project_id,
        content_type=ContentType.TEXT_TO_IMAGE,
        status=GenerationStatus.PROCESSING,
        prompt=request.prompt,
        parameters={
            "style": request.style,
            "aspect_ratio": request.aspect_ratio
        },
        started_at=datetime.utcnow()
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)
    
    try:
        # Call AI service
        result = await ai_service.generate_text_to_image(
            prompt=request.prompt,
            style=request.style,
            aspect_ratio=request.aspect_ratio,
            user_id=current_user.id
        )
        
        if result['success']:
            # Update generation record with results
            generation.status = GenerationStatus.COMPLETED
            generation.generated_content = result.get('content')
            generation.model_used = result.get('model_used')
            generation.processing_time = int(result.get('processing_time', 0))
            generation.completed_at = datetime.utcnow()
            generation.generation_metadata = {
                "images": result.get('images', []),
                "api_key_used": result.get('api_key_used')
            }
        else:
            generation.status = GenerationStatus.FAILED
            generation.generation_metadata = {"error": result.get('error')}
        
        db.commit()
        db.refresh(generation)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return generation
        
    except Exception as e:
        generation.status = GenerationStatus.FAILED
        generation.generation_metadata = {"error": str(e)}
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/product-render", response_model=ContentGenerationResponse)
async def generate_product_render(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    render_type: str = Form(...),
    instructions: str = Form(""),
    project_id: Optional[int] = Form(None),
    image: UploadFile = File(...)
):
    """Generate 3D render or professional product image"""
    
    # Validate file type
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read image data
    image_data = await image.read()
    
    # Create generation record
    content_type = ContentType.PRODUCT_3D_RENDER if render_type == "3d_render" else ContentType.PROFESSIONAL_PRODUCT
    
    generation = ContentGeneration(
        user_id=current_user.id,
        project_id=project_id,
        content_type=content_type,
        status=GenerationStatus.PROCESSING,
        prompt=instructions,
        parameters={
            "render_type": render_type,
            "original_filename": image.filename
        },
        started_at=datetime.utcnow()
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)
    
    try:
        # Call AI service
        result = await ai_service.generate_product_render(
            image_data=image_data,
            render_type=render_type,
            instructions=instructions,
            user_id=current_user.id
        )
        
        if result['success']:
            generation.status = GenerationStatus.COMPLETED
            generation.generated_content = result.get('content')
            generation.model_used = result.get('model_used')
            generation.processing_time = int(result.get('processing_time', 0))
            generation.completed_at = datetime.utcnow()
            generation.generation_metadata = {
                "images": result.get('images', []),
                "api_key_used": result.get('api_key_used')
            }
        else:
            generation.status = GenerationStatus.FAILED
            generation.generation_metadata = {"error": result.get('error')}
        
        db.commit()
        db.refresh(generation)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return generation
        
    except Exception as e:
        generation.status = GenerationStatus.FAILED
        generation.generation_metadata = {"error": str(e)}
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seo-content", response_model=ContentGenerationResponse)
async def generate_seo_content(
    request: SEOContentRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Generate SEO-optimized content"""
    
    generation = ContentGeneration(
        user_id=current_user.id,
        project_id=request.project_id,
        content_type=ContentType.SEO_CAPTION,
        status=GenerationStatus.PROCESSING,
        prompt=request.product_description,
        parameters={
            "target_keywords": request.target_keywords,
            "platform": request.platform
        },
        started_at=datetime.utcnow()
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)
    
    try:
        result = await ai_service.generate_seo_content(
            product_description=request.product_description,
            target_keywords=request.target_keywords,
            platform=request.platform,
            user_id=current_user.id
        )
        
        if result['success']:
            generation.status = GenerationStatus.COMPLETED
            generation.generated_content = result.get('content')
            generation.model_used = result.get('model_used')
            generation.processing_time = int(result.get('processing_time', 0))
            generation.completed_at = datetime.utcnow()
            generation.generation_metadata = {
                "api_key_used": result.get('api_key_used')
            }
        else:
            generation.status = GenerationStatus.FAILED
            generation.generation_metadata = {"error": result.get('error')}
        
        db.commit()
        db.refresh(generation)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return generation
        
    except Exception as e:
        generation.status = GenerationStatus.FAILED
        generation.generation_metadata = {"error": str(e)}
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/content-plan", response_model=ContentGenerationResponse)
async def generate_content_plan(
    request: ContentPlanRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Generate content calendar and plan"""
    
    generation = ContentGeneration(
        user_id=current_user.id,
        project_id=request.project_id,
        content_type=ContentType.CONTENT_PLAN,
        status=GenerationStatus.PROCESSING,
        prompt=request.product_info,
        parameters={
            "target_audience": request.target_audience,
            "goals": request.goals,
            "timeframe": request.timeframe
        },
        started_at=datetime.utcnow()
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)
    
    try:
        result = await ai_service.generate_content_plan(
            product_info=request.product_info,
            target_audience=request.target_audience,
            goals=request.goals,
            timeframe=request.timeframe,
            user_id=current_user.id
        )
        
        if result['success']:
            generation.status = GenerationStatus.COMPLETED
            generation.generated_content = result.get('content')
            generation.model_used = result.get('model_used')
            generation.processing_time = int(result.get('processing_time', 0))
            generation.completed_at = datetime.utcnow()
            generation.generation_metadata = {
                "api_key_used": result.get('api_key_used')
            }
        else:
            generation.status = GenerationStatus.FAILED
            generation.generation_metadata = {"error": result.get('error')}
        
        db.commit()
        db.refresh(generation)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return generation
        
    except Exception as e:
        generation.status = GenerationStatus.FAILED
        generation.generation_metadata = {"error": str(e)}
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/marketing-plan", response_model=ContentGenerationResponse)
async def generate_marketing_plan(
    request: MarketingPlanRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Generate comprehensive marketing plan"""
    
    generation = ContentGeneration(
        user_id=current_user.id,
        project_id=request.project_id,
        content_type=ContentType.MARKETING_PLAN,
        status=GenerationStatus.PROCESSING,
        prompt=request.product_info,
        parameters={
            "target_audience": request.target_audience,
            "goal": request.goal,
            "budget_range": request.budget_range,
            "timeline": request.timeline
        },
        started_at=datetime.utcnow()
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)
    
    try:
        result = await ai_service.generate_marketing_plan(
            product_info=request.product_info,
            target_audience=request.target_audience,
            goal=request.goal,
            budget_range=request.budget_range,
            timeline=request.timeline,
            user_id=current_user.id
        )
        
        if result['success']:
            generation.status = GenerationStatus.COMPLETED
            generation.generated_content = result.get('content')
            generation.model_used = result.get('model_used')
            generation.processing_time = int(result.get('processing_time', 0))
            generation.completed_at = datetime.utcnow()
            generation.generation_metadata = {
                "api_key_used": result.get('api_key_used')
            }
        else:
            generation.status = GenerationStatus.FAILED
            generation.generation_metadata = {"error": result.get('error')}
        
        db.commit()
        db.refresh(generation)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return generation
        
    except Exception as e:
        generation.status = GenerationStatus.FAILED
        generation.generation_metadata = {"error": str(e)}
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/generations", response_model=List[ContentGenerationResponse])
def get_user_generations(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get user's content generations"""
    generations = db.query(ContentGeneration).filter(
        ContentGeneration.user_id == current_user.id
    ).order_by(ContentGeneration.created_at.desc()).offset(skip).limit(limit).all()
    
    return generations

@router.get("/generations/{generation_id}", response_model=ContentGenerationResponse)
def get_generation(
    generation_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """Get specific generation by ID"""
    generation = db.query(ContentGeneration).filter(
        ContentGeneration.id == generation_id,
        ContentGeneration.user_id == current_user.id
    ).first()
    
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    
    return generation